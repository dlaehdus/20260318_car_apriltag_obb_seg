yolo26x-seg, obb로 학습하여 에어프릴태그의 알고리즘을 적용하는게 이전의 프로젝트의 각 숫자별로 영상처리를 통해obb알고리즘을 적용하는것보다 정확도가 높을것으로 예상하고 시작한 프로젝트

현재 대한민국 차량 번호판의 obb데이터셋은 많이 풀리지 않음 따라서 1000장 이상의 데이터를 확보하기 위해서 자료조사중 세그멘테이션이된 1000장을 찾음 따라서 이 데이터셋을 전처리를 통해 obb데이터셋으로 교체후 학습할것임
https://universe.roboflow.com/school-2whgn/korea-carplate/dataset/3

obb_trade.py파일을 실행하면
해당 labels들의 seg된 점들이 obb로 변환됨

잘 되었는지 확인하기 위해 draw_labels로 해당 파일들을 점검함

세그멘테이션 되어있는 데이터

<img width="593" height="558" alt="image" src="https://github.com/user-attachments/assets/36564fc2-65ad-4be8-8269-c099372176e9" />

obb로 전환한 데이터

<img width="593" height="558" alt="image" src="https://github.com/user-attachments/assets/0ec73fea-4b21-48dc-a993-0a489872f090" />

세그멘테이션 되어있는 데이터

<img width="593" height="558" alt="image" src="https://github.com/user-attachments/assets/a675d483-6f0e-491a-8e2f-0f6ae0462416" />

obb로 전환한 데이터

<img width="593" height="558" alt="image" src="https://github.com/user-attachments/assets/fe419dfd-90f5-42eb-a9e6-ea21f43db30d" />

세그멘테이션 되어있는 데이터

<img width="593" height="558" alt="image" src="https://github.com/user-attachments/assets/0f3f30b0-870d-4a55-9cf5-0d23e859c411" />

obb로 전환한 데이터

<img width="593" height="558" alt="image" src="https://github.com/user-attachments/assets/fd534a45-b844-4601-b96f-951a108ecdf6" />


위의 방법을 사용해서 세그멘테이션 자료를 obb로 전환하여 학습을 진행하였지만 에어프릴태그의 논리를 적용할 정도로 정밀하게 사각형 박스가 채워지지 않음
<img width="447" height="183" alt="image" src="https://github.com/user-attachments/assets/98cd9207-627c-4bf1-a4cb-f2b759de37da" />

위의 사진의 오른쪽 상단처럼 살짝 비껴가는 경우가 발생함 이유를 찾아보니 세그멘테이션 자료를 obb데이터로 변환할때 알고리즘에 이미지처리 필터를 통해 좀더 정밀한 전처리를 해야했음
평균값을 활용해 정밀하게 다시 데이터 전처리 알고리즘을 작성하는 방법 
또는 seg자료를 영상처리를 통해 obb처럼 만드는경우 2가지를 테스트 해볼것임




