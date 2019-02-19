import cv2
import os

def create_video(image_folder, video_name, fps=8, reverse=False):
    #create video out of images saved in a folder
    images = [img for img in os.listdir(image_folder) if img.endswith('.jpg')]
    #images = images[::10]
    #images.sort(key=os.path.getmtime)
    if reverse: images = images[::-1]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, -1, fps, (width,height))
    for image in images:
        print('wrote '+format(image))
        video.write(cv2.imread(os.path.join(image_folder, image)))
        
    cv2.destroyAllWindows()
    video.release()
    


#%% combine figs into video

video_name = r'C:\Users\Eric\Desktop\brew_timelapse.avi'
image_folder = 'brew_plots'

make_video = True
if make_video: create_video(image_folder, video_name, fps=8)