import cv2
import numpy as np
import os
from pathlib import Path

def batch_visualize_and_save(base_path, split="test"):
    img_dir = Path(base_path) / split / "images"
    lbl_dir = Path(base_path) / split / "labels"
    save_dir = Path(base_path) / split / "visualization_results"
    os.makedirs(save_dir, exist_ok=True)

    img_files = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg"))
    
    print(f"총 {len(img_files)}개의 이미지 시각화 시작")

    for img_path in img_files:
        img = cv2.imread(str(img_path))
        if img is None: continue
        
        h, w, _ = img.shape
        
        lbl_path = lbl_dir / (img_path.stem + ".txt")
        
        if lbl_path.exists():
            with open(lbl_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                parts = list(map(float, line.strip().split()))
                if not parts: continue
                
                class_id = int(parts[0])
                coords = parts[1:]
                
                points = []
                for i in range(0, len(coords), 2):
                    px = int(coords[i] * w)
                    py = int(coords[i+1] * h)
                    points.append((px, py))
                
                pts_array = np.array(points, np.int32).reshape((-1, 1, 2))
                
                cv2.polylines(img, [pts_array], isClosed=True, color=(0, 255, 0), thickness=2)

                for idx, (px, py) in enumerate(points):
                    cv2.circle(img, (px, py), 4, (0, 0, 255), -1)
                    cv2.putText(img, str(idx), (px + 5, py - 5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

                cv2.putText(img, f"ID:{class_id}", (points[0][0], points[0][1]-20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        save_path = save_dir / img_path.name
        cv2.imwrite(str(save_path), img)
        print(f"저장 완료: {save_path.name}")

base_path = "/home/limdoyeon/Downloads/Korea CarPlate.v3i.yolov12/"
batch_visualize_and_save(base_path, "train")

print("\n 모든 시각화 결과가 'visualization_results' 폴더에 저장되었습니다!")