import cv2
import numpy
import time

pointerImg = cv2.imread("RedPointer.jpg")
pointerImg = cv2.resize(pointerImg,(200,200))
arrow = cv2.imread("backArrow.png")
arrow = cv2.resize(arrow,(100,50))
background = cv2.imread("OrigImage.png")
background = cv2.resize(background, (1200,750))
cv2.putText(background, "Instructions:", (50, 430), cv2.FONT_ITALIC, 1, (200, 0, 0))
cv2.putText(background, "- On the next page, hover over an article's title to access it.", (50, 460), cv2.FONT_ITALIC, 0.9, (200, 0, 0))
cv2.putText(background, "- Scroll through the article by hovering the pointer at the top or", (50, 500), cv2.FONT_ITALIC, 0.9, (200, 0, 0))
cv2.putText(background, "bottom of the page and swipe from left to right to view multiple", (50, 530), cv2.FONT_ITALIC, 0.9, (200, 0, 0))
cv2.putText(background, "images that relate to one topic.", (50, 560), cv2.FONT_ITALIC, 0.9, (200, 0, 0))
cv2.putText(background, "- Hover over the 'Puzzles' side bar to access it (Instructions to", (50, 600), cv2.FONT_ITALIC, 0.9, (200, 0, 0))
cv2.putText(background, "solve the Sudoku are on the Puzzles page)", (50, 630), cv2.FONT_ITALIC, 0.9, (200, 0, 0))

min = [(490,260),(0,110),(0,260),(460,260),(0,420),(500,420),(0,570),(610,570),(1100,0)]
max = [(640,370),(1100,260),(460,420),(1100,420),(500,570),(1100,570),(610,700),(1100,700),(1200,700)]
pageImg = [cv2.imread("TrumpDeclaresWar.png"),cv2.imread("LifeFoundOnMars.png"),cv2.imread("InmatesEscape.png"),
           cv2.imread("DirtyLawyers.png"),cv2.imread("MethaneEmissions.png"),cv2.imread("RowlingSecret.png"),
           cv2.imread("ClimateChange.png"),cv2.imread("Sudoku.png")]
articlePics = [cv2.imread("1.png"),cv2.imread("2.png"),cv2.imread("3.png"),cv2.imread("4.png"),cv2.imread("5.png"),cv2.imread("6.png"),cv2.imread("7.png"),cv2.imread("8.png"),cv2.imread("9.png")]

sudokuPics = [cv2.imread("1.png"),cv2.imread("2.png"),cv2.imread("3.png"),cv2.imread("4.png"),cv2.imread("5.png"),cv2.imread("6.png"),cv2.imread("7.png"),cv2.imread("8.png"),cv2.imread("9.png")]
correctLoc = [(1,1),(2,1),(3,1),(4,1),(8,1),(9,1),(1,2),(2,2),(3,2),(5,2),(6,2),(7,2),(8,2),(9,2),(2,3),(4,3),(5,3),(8,3),(9,3),(2,4),(4,4),(5,4),(6,4),(7,4),(9,4),(2,5),(3,5),(4,5),(6,5),(7,5),(8,5),
              (1,6),(3,6),(4,6),(5,6),(6,6),(8,6),(1,7),(2,7),(5,7),(6,7),(8,7),(1,8),(2,8),(3,8),(4,8),(7,8),(8,8),(9,8),(1,9),(2,9),(6,9),(7,9),(8,9),(9,9)]
sudokuNumMin = [(160,100),(160,230),(160,360),(160,490),(160,620),(1000,165),(1000,295),(1000,425),(1000,555)]
sudokuNumMax = [(220,165),(220,295),(220,425),(220,555),(220,685),(1060,230),(1060,360),(1060,490),(1060,620)]
for i in range(0,9):
    articlePics[i] = cv2.resize(articlePics[i],(400,200))
page = 0

def getNextFrame(vidObj):
    ret, frame = vidObj.read()
    frame = frame[:, ::-1, :]
    return frame

cam = cv2.VideoCapture(0)

track_window=(0,0,1200,700)
hist = cv2.calcHist([pointerImg], [0],None, [16], [0, 256])
cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
hist = hist.reshape(-1)
bin_count = hist.shape[0]
bin_w = 24
img = numpy.zeros((256, bin_count * bin_w, 3), numpy.uint8)
for i in xrange(bin_count):
    h = int(hist[i])
    cv2.rectangle(img, (i * bin_w + 2, 255), ((i + 1) * bin_w - 2, 255 - h), (int(180.0 * i / bin_count), 255, 255), -1)
img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
cv2.imshow('hist', img)

prevLocation = (0.,0.)
oldtime = time.time()
radius = 10.0
pageChosen = None
articleSwipe = 0
picSwipe = 0
chosenArticlePic = 0

sudoku = 0
sudokuChosen=None
sudokuLoc = 0
finalSol = [0]*55
correctSol = [8,5,1,3,2,4,4,3,9,1,2,6,5,7,6,4,9,8,3,4,1,3,9,7,8,1,6,7,4,2,9,9,8,2,5,6,4,1,9,4,8,7,5,8,7,9,4,3,6,6,2,3,8,1,9]

while True:
    frame = getNextFrame(cam)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, numpy.array((0., 60., 32.)),
                       numpy.array((180., 255., 255.)))
    prob = cv2.calcBackProject([hsv], [0], hist, [0, 256], 1)
    prob &= mask
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    track, track_window = cv2.CamShift(prob, track_window, term_crit)
    track_box=(((track[0][0]-200)*8/7,(track[0][1]-100)*6/5),(track[1][0],track[1][1]),track[2])

    if prevLocation[0] <= track_box[0][0]+10 and prevLocation[1] <= track_box[0][1]+10 and prevLocation[0] >= track_box[0][0]-10 and prevLocation[0] >= track_box[0][0]-10:
        if page == 2:
            if 0 < track_box[0][0] and 200 > track_box[0][0] and 0 < track_box[0][1] and 100 > track_box[0][1]:
                radius += 1.5
                if time.time() - oldtime > 1:
                    background = cv2.imread("coverpage.png")
                    background = cv2.resize(background, (1200, 750))
                    articleSwipe=0
                    chosenArticlePic=0
                    page -= 1
            else:
                pageChosen[90:290, 80:480] = articlePics[chosenArticlePic]
                background = pageChosen[articleSwipe:400 + articleSwipe, 0:background.shape[1]]
                background = cv2.resize(background, (1200, 750))
                background[10:arrow.shape[0] + 10, 10:arrow.shape[1] + 10] = arrow
            if 550<=track_box[0][1]:
                if pageChosen.shape[0]-400>articleSwipe:
                    articleSwipe+=16
                pageChosen[90:290, 80:480] = articlePics[chosenArticlePic]
                background = pageChosen[articleSwipe:400 + articleSwipe, 0:background.shape[1]]
                background = cv2.resize(background, (1200, 750))
                background[10:arrow.shape[0] + 10, 10:arrow.shape[1] + 10] = arrow
            elif 150>=track_box[0][1]:
                if 0<articleSwipe:
                    articleSwipe-=16
        elif page==3:
            radius += 1.5
            if 0 < track_box[0][0] and 200 > track_box[0][0] and 0 < track_box[0][1] and 100 > track_box[0][1]:
                radius += 1.5
                if time.time() - oldtime > 1:
                    background = cv2.imread("coverpage.png")
                    background = cv2.resize(background, (1200, 750))
                    articleSwipe=0
                    chosenArticlePic=0
                    page -= 2
            if time.time() - oldtime > 1:
                if 1040 < track_box[0][0] and 1160 > track_box[0][0] and 20 < track_box[0][1] and 150 > track_box[0][1]:
                    score = 0
                    for count in range(0,55):
                        if finalSol[count]==correctSol[count]:
                            score+=1
                    fs = str(int(score*100.0/55))
                    cv2.putText(background, "Your answer is " + fs + "% correct!", (960, 200), cv2.FONT_ITALIC, 0.5,(200, 0, 0))
                if 1040 < track_box[0][0] and 1160 > track_box[0][0] and 550 < track_box[0][1] and 680 > track_box[0][1]:
                    pageChosen = cv2.imread("Sudoku.png")
                    background = cv2.resize(pageChosen, (1200, 750))
                    background[10:arrow.shape[0] + 10, 10:arrow.shape[1] + 10] = arrow
                    finalSol = [0] * 55
                if sudoku==1:
                    for i in range (0,9):
                        if track_box[0][0]>sudokuNumMin[i][0] and track_box[0][0]<sudokuNumMax[i][0] and track_box[0][1]>sudokuNumMin[i][1] and track_box[0][1]<sudokuNumMax[i][1]:
                            num = cv2.resize(sudokuPics[i], (50,50))
                            pageChosen[sudokuChosen[1]*67/66+5:sudokuChosen[1]*67/66+5+50, int(sudokuChosen[0]*66.1/68)-5:int(sudokuChosen[0]*66.1/68)+50-5] = num
                            background = cv2.resize(pageChosen, (1200, 750))
                            background[10:arrow.shape[0] + 10, 10:arrow.shape[1] + 10] = arrow
                            index = correctLoc.index(sudokuLoc)
                            finalSol[index] = i+1
                            sudoku = 0
                for x in range (1,10):
                    for y in range(1,10):
                        if track_box[0][0]>308+(x-1)*68 and track_box[0][0]<308+x*68 and track_box[0][1]>105+(y-1)*66 and track_box[0][1]<105+y*66:
                            if((x==1 and y>=3 and y<=5) or (y==9 and x>=3 and x<=5) or (y==1 and x>=5 and x<=7) or (x==9 and y>=5 and y<=7) or
                                    (y==6 and (x==2 or x==7)) or (y==8 and x>=5 and x<=6) or (y==7 and (x==3 or x==4 or x==7)) or (y==5 and x==5)
                                    or (y==4 and (x==3 or x==8)) or (y==3 and (x==3 or x==6 or x==7)) or (y==2 and x==4)):
                                background = cv2.resize(pageChosen, (1200, 750))
                                background[10:arrow.shape[0] + 10, 10:arrow.shape[1] + 10] = arrow
                                cv2.putText(background, "Please select an editable box.", (390, 730), cv2.FONT_ITALIC, 0.9, (200, 0, 0))
                            else:
                                background = cv2.resize(pageChosen, (1200, 750))
                                sudokuChosen = (308+(x-1)*68, 105+(y-1)*66)
                                cv2.rectangle(background, (308+(x-1)*68, int(105+(y-1)*65.5)), (308+x*68, int(105+y*65.5)), (240, 0, 0), 2)
                                background[10:arrow.shape[0] + 10, 10:arrow.shape[1] + 10] = arrow
                                sudoku = 1
                                sudokuLoc = (x,y)
                oldtime = time.time()
                radius = 10
        else:
            radius+=1.5
        if time.time() - oldtime > 1:
            if page==0:
                if min[0][0]<track_box[0][0] and max[0][0]>track_box[0][0] and min[0][1]<track_box[0][1] and max[0][1]>track_box[0][1]:
                    background=cv2.imread("coverpage.png")
                    background = cv2.resize(background, (1200, 750))
                    page+=1
            elif page==1:
                for i in range(1, 9):
                    if min[i][0] < track_box[0][0] and max[i][0] > track_box[0][0] and min[i][1] < track_box[0][1] and max[i][1] > track_box[0][1]:
                        pageChosen = pageImg[i-1]
                        if i==8:
                            page+=1
                            background = cv2.resize(pageChosen, (1200,750))
                        else:
                            pageChosen[90:290, 80:480] = articlePics[chosenArticlePic]
                            background = pageChosen[0:400, 0:background.shape[1]]
                            background = cv2.resize(background, (1200,750))
                        background[10:arrow.shape[0]+10, 10:arrow.shape[1]+10] = arrow
                        page+=1
            oldtime = time.time()
            radius = 10
    elif page == 2:
        if track_box[0][1] < prevLocation[1] + 15 and track_box[0][1] > prevLocation[1] - 15:
            if track_box[0][0] > prevLocation[0] + 20:
                picSwipe += 1
                if picSwipe > 5:
                    if chosenArticlePic<8:
                        chosenArticlePic += 1
                    else:
                        chosenArticlePic = 0
                    picSwipe = 0
            #elif track_box[0][0] < prevLocation[0] - 20:
                #picSwipe -= 1
                #if picSwipe < -6:
                    #if chosenArticlePic>0:
                        #chosenArticlePic -= 1
                    #picSwipe = 0
        oldtime = time.time()
        radius = 10
    else:
        oldtime = time.time()
        radius = 10

    backgroundCopy = background.copy()
    cv2.ellipse(backgroundCopy, (track_box[0], (radius, radius), 80), (0, 0, 255), -1)
    cv2.imshow('Newspaper', backgroundCopy)
    cv2.moveWindow('Newspaper', 50, 0)

    prevLocation = track_box[0]
    ch = chr(0xFF & cv2.waitKey(10))
    if ch == 'q':
        break

cv2.destroyAllWindows()
cam.release()