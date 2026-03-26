import cv2
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def main():
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=1
    )
    detector = vision.HandLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        # 2. Convert and Detect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp = int(time.time() * 1000)
        result = detector.detect_for_video(mp_image, timestamp)
        # 3. Handle Results (Minimal manual drawing if mp.solutions is missing)
        if result.hand_landmarks:
            for landmarks in result.hand_landmarks:
                index_pos = [5, 6, 7, 8] # Index finger landmarks
                index_lm = [landmarks[i] for i in index_pos]
                print(f'''
Index finger landmarks:
5: {index_lm[0].y} === 6: {index_lm[1].y} === 7: {index_lm[2].y} === 8: {index_lm[3].y}
5-6: {index_lm[0].y - index_lm[1].y} === 6-7: {index_lm[1].y - index_lm[2].y} === 7-8: {index_lm[2].y - index_lm[3].y}

5: {index_lm[0].x} === 6: {index_lm[1].x} === 7: {index_lm[2].x} === 8: {index_lm[3].x}
5-6: {index_lm[1].x - index_lm[0].x} === 6-7: {index_lm[2].x - index_lm[1].x} === 7-8: {index_lm[3].x - index_lm[2].x}
''')
                if index_lm[0].y < index_lm[3].y:
                    print("Index finger is down")
                elif index_lm[3].y < index_lm[0].y and (index_lm[3].y >= index_lm[2].y or index_lm[2].y >= index_lm[1].y or (index_lm[2].y) - (index_lm[3].y) < 0.035 or (index_lm[1].y) - (index_lm[2].y) < 0.035):
                    print("Index finger is bent")
                elif index_lm[1].y > index_lm[2].y > index_lm[3].y:
                    print("Index finger is up")
                else:
                    print("Index finger is in an unknown position") 

                # for index, lm in enumerate(landmarks):
                #     print(f'{index+1}: {lm}')
                #     # Draw a simple circle at each landmark point
                #     h, w, _ = frame.shape
                #     cx, cy = int(lm.x * w), int(lm.y * h)
                #     cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        cv2.imshow('M4 Hand Tracking', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

        time.sleep(1)

    detector.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


'''
output: 
HandLandmarkerResult(
    handedness=[
        [
            Category(
                index=0, 
                score=0.9748417139053345, 
                display_name='Right', 
                category_name='Right'
            )
        ]
    ], 
    hand_landmarks=[
        [
            NormalizedLandmark(x=0.17500095069408417, y=0.8444004058837891, z=1.2630296453153278e-07, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.19864097237586975, y=0.8924791216850281, z=-0.008540033362805843, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.20855560898780823, y=0.9639626145362854, z=-0.01858053356409073, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.20835915207862854, y=1.026651382446289, z=-0.025462552905082703, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.20727738738059998, y=1.0690665245056152, z=-0.0319676473736763, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.1876007616519928, y=0.9458968043327332, z=-0.04288872331380844, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.17309057712554932, y=1.0393648147583008, z=-0.05307072028517723, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.16491976380348206, y=1.0767443180084229, z=-0.05209473893046379, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.15999376773834229, y=1.0973129272460938, z=-0.049513667821884155, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.16038306057453156, y=0.9340988397598267, z=-0.04204309359192848, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.13575774431228638, y=1.0242918729782104, z=-0.051006924360990524, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.1306172013282776, y=1.062324047088623, z=-0.04708757624030113, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.13022880256175995, y=1.0817372798919678, z=-0.044077858328819275, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.13723386824131012, y=0.927428662776947, z=-0.039577506482601166, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.11316019296646118, y=1.0132555961608887, z=-0.04656997323036194, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.11069472134113312, y=1.0530542135238647, z=-0.040184635668992996, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.11168138682842255, y=1.0773890018463135, z=-0.035293396562337875, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.11953706294298172, y=0.9264605045318604, z=-0.036665406078100204, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.0986454114317894, y=0.9991474151611328, z=-0.041214678436517715, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.09456299990415573, y=1.032992959022522, z=-0.03633536025881767, visibility=None, presence=None, name=None), 
            NormalizedLandmark(x=0.09496451914310455, y=1.0549707412719727, z=-0.031898148357868195, visibility=None, presence=None, name=None)
        ]
    ], 
    hand_world_landmarks=[
        [
            Landmark(x=0.00708559388294816, y=-0.027791181579232216, z=0.07930368930101395, visibility=None, presence=None, name=None), 
            Landmark(x=0.018462587147951126, y=-0.007971436716616154, z=0.05582587420940399, visibility=None, presence=None, name=None), 
            Landmark(x=0.016350002959370613, y=0.011423332616686821, z=0.04286679998040199, visibility=None, presence=None, name=None), 
            Landmark(x=0.02577134594321251, y=0.02357703074812889, z=0.018598759546875954, visibility=None, presence=None, name=None), 
            Landmark(x=0.027950847521424294, y=0.03687309846282005, z=0.002718136180192232, visibility=None, presence=None, name=None), 
            Landmark(x=0.007877938449382782, y=0.00935389008373022, z=-0.0020214735995978117, visibility=None, presence=None, name=None), 
            Landmark(x=0.004319409374147654, y=0.020416636019945145, z=-0.0044730850495398045, visibility=None, presence=None, name=None), 
            Landmark(x=0.0018502091988921165, y=0.03864990919828415, z=0.006108015310019255, visibility=None, presence=None, name=None), 
            Landmark(x=0.00022642314434051514, y=0.043911706656217575, z=0.026477303355932236, visibility=None, presence=None, name=None), 
            Landmark(x=0.0016480134800076485, y=0.0009299897355958819, z=-0.0029424172826111317, visibility=None, presence=None, name=None), 
            Landmark(x=-0.008609124459326267, y=0.015375124290585518, z=-0.007981963455677032, visibility=None, presence=None, name=None), 
            Landmark(x=-0.010062219575047493, y=0.029593605548143387, z=0.0063151149079203606, visibility=None, presence=None, name=None), 
            Landmark(x=-0.012908539734780788, y=0.04197681322693825, z=0.03222000598907471, visibility=None, presence=None, name=None), 
            Landmark(x=-0.0027443664148449898, y=-0.005117139779031277, z=0.0013515723403543234, visibility=None, presence=None, name=None), 
            Landmark(x=-0.011587685905396938, y=0.006551450118422508, z=-0.0044896467588841915, visibility=None, presence=None, name=None), 
            Landmark(x=-0.02062823809683323, y=0.021268315613269806, z=0.011241210624575615, visibility=None, presence=None, name=None), 
            Landmark(x=-0.02189820073544979, y=0.034811265766620636, z=0.03268938511610031, visibility=None, presence=None, name=None), 
            Landmark(x=-0.008135166950523853, y=-0.012232085689902306, z=0.013911310583353043, visibility=None, presence=None, name=None), 
            Landmark(x=-0.01880544237792492, y=0.0008648466318845749, z=0.009904707781970501, visibility=None, presence=None, name=None), 
            Landmark(x=-0.025190703570842743, y=0.014984994195401669, z=0.02018681913614273, visibility=None, presence=None, name=None), 
            Landmark(x=-0.02549072355031967, y=0.029285607859492302, z=0.03196162357926369, visibility=None, presence=None, name=None)
        ]
    ]
)
'''
