shots_queue = []
frames = []

##
# What it says on the tin
# frames -> frame list
def print_frames(frames):
    it = 0
    print()
    for frame in frames:
        print(f'Frame {it + 1} result')
        print('-' * 15)
        print(f'{frame["shots"]:9} || {frame["score"]:>5}')
        print()
        it += 1
    print('\n')

##
# Calcuate the scores recursively for each frame, updates previous frames w/ spares and strikes
# shots -> the shots list
# frame -> the current frame being evaluated
# score -> variable for storing current score
def calculate_score(shots, frame = 1, score = 0):
    
    # return out
    if frame > 10 or not shots:
        return score
    
    # Strike
    elif shots[0] == 10:
        bonus = 0

        # we have the next 2 shot data, add them for the bonus
        if len(shots) > 2:
            bonus = shots[1] + shots[2]
        # we only have 1 score so far, so add that to the bonus
        # for now, will re-evaluate after the next frame
        elif len(shots) > 1:
            bonus = shots[1]
        
        new_score = score + 10 + bonus

        # We don't want to update if we're on the current frame, or the first frame
        if len(frames) > frame - 1:
            # we need to update a previous frame because it may have had incomplete data
            frames[frame - 1]['score'] = new_score

        # goto next frame, only need to remove 1 shot since this frame only has an X
        return calculate_score(shots[1:], frame + 1, new_score)
    
    # Spare
    elif (shots[0] + shots[1]) == 10:
        bonus = 0

        # if we have the next frame to score, we add to the bonus
        if len(shots) > 2:
            bonus = shots[2]
        
        new_score = score + 10 + bonus

        # We don't want to update if we're on the current frame, or the first frame
        if len(frames) > frame - 1:
            # we need to update a previous frame because it may have had incomplete data
            frames[frame - 1]['score'] = new_score
        
        # go to next frame
        return calculate_score(shots[2:], frame + 1, new_score)
    
    # Open
    else:
        score += shots[0] + shots[1]

        # it's an open frame so no special logic, add to score and return
        return calculate_score(shots[2:], frame + 1, score)

## 
# add a frame to the frames list which is used to print the frames
# as they arrive and stores the score and shots
def add_frames(shots):
    global frames

    # this frame is not the 10th frame
    if len(frames) < 9:
        if shots[0] in 'xX':
            shots_queue.append(10)
        elif shots[1] == '/':
            shots_queue.append(int(shots[0]))
            shots_queue.append(10 - int(shots[0]))
        else:
            shots_queue.append(int(shots[0]))
            shots_queue.append(int(shots[1]))
    #this is the 10th frame
    elif len(frames) == 9:
        if len(shots) < 3:
            shots_queue.append(int(shots[0]))
            shots_queue.append(int(shots[1]))
        else:
            # if it's 3 shots it can be:
            # 3 strikes
            # a strike and a spare
            # a strike and 2 open shots
            # a spare + 1 shot (strike or open)

            # 3 strikes is 30 points
            if shots[0] in 'xX' and shots[1] in 'xX' and shots[2] in 'xX':
                shots_queue.append(10)
                shots_queue.append(10)
                shots_queue.append(10)

            # it's not 3 strikes, so it could be a strike and a spare or a strike and 2 open
            elif shots[0] in 'xX':
                shots_queue.append(10)

                # next 2 could be a spare or open
                if shots[2] == '/':
                    shots_queue.append(int(shots[1]))
                    shots_queue.append(10 - int(shots[1]))
                else:
                    shots_queue.append(int(shots[1]))
                    shots_queue.append(int(shots[2]))
            
            # if the frame doesn't start with a strike, we look for 
            elif shots[1] == '/':
                shots_queue.append(int(shots[0]))
                shots_queue.append(10 - int(shots[0]))
                # last shot could be a strike or an open
                if shots[2] in 'xX':
                    shots_queue.append(10)
                else:
                    shots_queue.append(int(shots[2]))
    
    # there's probably a better way to do with with list comprehension
    if len(shots) == 1:
        shots_string = f'{shots[0]}'
    elif len(shots) == 2:
        shots_string = f'{shots[0]} | {shots[1]}'
    elif len(shots) == 3:
        shots_string = f'{shots[0]} | {shots[1]} | {shots[2]}'
    
    frames.append({"shots":shots_string, "score": f'{calculate_score(shots_queue)}'})

def main():
    for i in range(10):
        print(f'Frame {i + 1}')
        shot_one = input('First shot: ')
        if shot_one not in 'xX' and i != 9:
            shot_two = input('Second shot: ')
        else:
            shot_two = input('Second shot: ')
        if i == 9 and (shot_one in 'xX' or shot_two == '/'):
            shot_three = input('Third shot: ')            
        
        shots_in_frame = []
        shots_in_frame.append(shot_one)

        if 'shot_two' in locals():
            shots_in_frame.append(shot_two)
            shot_two = ''
        
        if 'shot_three' in locals():
            shots_in_frame.append(shot_three)
        

        add_frames(shots_in_frame)

        print_frames(frames)

# Turning this in as is
# Missing:
# - Tests for the different functionality
# - Better UI
# - Regex for validating input
# - Loop to improve re-inputing when data is invalid
# - Breaking logic into it's own class to eliminate globals

if __name__ == '__main__':
    main()