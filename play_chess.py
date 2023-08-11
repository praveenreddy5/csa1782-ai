import cv2
import numpy as np
import json
import chess
import chess.svg
from cairosvg import svg2png
import chess.engine
from arm import ChessRobotArm
import random

engine = chess.engine.SimpleEngine.popen_uci(r"stockfish\stockfish-windows-2022-x86-64-avx2.exe")

with open('sqdict.json', 'r') as fp:
    sq_points = json.load(fp)

# Returns the square given a point within the square
def find_square(x: float, y: float): 
    for square in sq_points:
        points = np.array(sq_points[square], np.int32)
        if cv2.pointPolygonTest(points, (x, y), False) > 0:
            return square
    return None

# Outline the squares
def draw_outlines(sq_points: dict, frame, show_text = False) -> None:
    for square in sq_points:
        points = sq_points[square]
        points = np.array(points, dtype=np.int32)
        cv2.polylines(frame, [points], True, (255, 255, 255), thickness=1)
        x, y, w, h = cv2.boundingRect(points)
        if show_text:
            cv2.putText(frame, square, (x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Show board using python-chess SVGRendering
def show_board(board: chess.Board, size=900, move=None) -> None:
    if move is not None:
        sq1, sq2 = chess.parse_square(move[:2]), chess.parse_square(move[2:4])
        svgwrap = chess.svg.board(board, size=size, fill=dict.fromkeys([sq1, sq2], '#ced264'))
    else:
        svgwrap = chess.svg.board(board, size=size)
    svg2png(svgwrap, write_to='output.png')
    cv2.imshow('Game', cv2.imread('output.png')) 

cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

initial = []
final = []
bounding_boxes = []
centers = []
highlights = set()

board = chess.Board()
robot = ChessRobotArm(22, 22.5, port='COM4')  # Initialize a 3DOF Robotic Arm with L1=22, L2=21, at port COM4
comp_move = True
show_board(board)
cv2.waitKey(2)

while not board.is_game_over():
    ret, frame = cap.read()
    draw_outlines(sq_points, frame)
    cv2.imshow('Frame', frame)

    if comp_move:
        result = engine.play(board, chess.engine.Limit(time=random.random()))
        comp_move = result.move.uci()
        (sq1, sq2) = (comp_move[:2], comp_move[2:4])

        # Check for castling
        if board.is_capture(result.move):
            robot.discard(sq2)

        # For straight pawn moves:
        robot.move(sq1, sq2, knight=(board.piece_type_at(chess.parse_square(sq1)) == chess.KNIGHT))

        if comp_move == 'e1g1' and board.piece_type_at(chess.E1) == chess.KING:  # Kingside
            robot.move('h1', 'f1')
        elif comp_move == 'e1c1' and board.piece_type_at(chess.E1) == chess.KING:  # Queenside
            robot.move('a1', 'd1')

        board.push(result.move)
        print('Robot plays', result.move.uci())
        show_board(board, move=str(result.move))
        comp_move = False

    for (x, y, w, h) in bounding_boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    for (x, y) in centers:
        square = find_square(x, y)
        highlights.add(square)

    # User interaction to change position or capture piece
    user_input = cv2.waitKey(1) & 0xFF
    if user_input == ord('c'):
        # Capture a piece
        print("Select a piece to capture...")
        while True:
            cv2.imshow('Frame', frame)
            user_capture_input = cv2.waitKey(1) & 0xFF
            if user_capture_input == ord('q'):
                break  # Exit capture mode
            elif user_capture_input == ord('c'):
                print("Capture move recorded.")
                # Process the captured move and perform the capture using the robot arm
                captured_square = find_square(x, y)  # Get the square where the piece was captured
                if captured_square:
                    print(f"Captured piece at square {captured_square}")
                    # Implement robotic arm action to capture the piece
                    # Update the board and display it
                    show_board(board)
                    comp_move = True
                    break
    elif user_input == ord('p'):
        # Change the position of a piece
        print("Select a piece to move...")
        while True:
            cv2.imshow('Frame', frame)
            user_move_input = cv2.waitKey(1) & 0xFF
            if user_move_input == ord('q'):
                break  # Exit move mode
            elif user_move_input == ord('m'):
                print("Move recorded.")
                # Process the move and perform it using the robot arm
                # Update the board and display it
                show_board(board)
                comp_move = True
                break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Frame', frame)

show_board(board)

# Release the video capture object
cap.release()

# Close all windows
cv2.destroyAllWindows()

