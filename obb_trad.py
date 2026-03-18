import os
import cv2
import numpy as np
from pathlib import Path

base_dir = "/home/limdoyeon/Downloads/Korea CarPlate.v3i.yolov12/"
epsilon_factor = 0.015

for split in ["train", "test", "valid"]:
    in_path = Path(base_dir) / split / "labels"
    out_path = Path(base_dir) / split / "labels"
    
    os.makedirs(out_path, exist_ok=True)

    txt_files = list(in_path.glob("*.txt"))
    if not txt_files:
        print(f"{split}/labels 폴더에 txt 파일이 없거나 경로가 틀립니다.")
        continue

    for txt in txt_files:
        with open(txt, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if not line.strip():
                continue
            data = list(map(float, line.strip().split()))
            cls = int(data[0])
            pts = np.array(data[1:]).reshape(-1, 2)

            if len(pts) < 3:
                continue

            hull = cv2.convexHull(pts.astype(np.float32))

            if len(hull) < 3:
                continue

            perimeter = cv2.arcLength(hull, True)
            epsilon = epsilon_factor * perimeter
            approx = cv2.approxPolyDP(hull, epsilon, True)

            if len(approx) != 4:
                epsilon = epsilon * 1.3
                approx = cv2.approxPolyDP(hull, epsilon, True)
                if len(approx) != 4:
                    rect = cv2.minAreaRect(pts.astype(np.float32))
                    box = cv2.boxPoints(rect)
                    box_norm = box.flatten().tolist()
                    print(f"   → {txt.name} fallback to minAreaRect")
                else:
                    box_norm = approx.reshape(-1).tolist()
            else:
                box_norm = approx.reshape(-1).tolist()

            new_line = [cls] + [round(float(x), 8) for x in box_norm]
            new_lines.append(" ".join(map(str, new_line)) + "\n")

        txt.write_text("".join(new_lines))
        print(f"변환 완료: {split}/labels/{txt.name}  (4점 quadrilateral 생성)")

print("\n모든 세그멘테이션 라벨이 YOLO OBB용 4점 quadrilateral로 제대로 변환되었습니다!")
print("   (마름모, 사다리꼴, 기울어진 모양 모두 반영됨)")