# Apple Quality AI

# apple-quality-ai-detector
AI powered image classification system for detecting fresh and formalin-mixed apples using deep learning and Streamlit.

## Overview

Formalin is sometimes illegally used as a preservative to keep fruit looking fresh for longer, which poses a health risk to consumers. This project builds a binary image classifier that distinguishes **Fresh** apples from **Formalin-mixed** apples using convolutional neural networks, and ships the trained model as an interactive Streamlit web app so anyone can upload a photo of an apple and get an instant prediction.

The full workflow — dataset acquisition, cleaning, exploratory data analysis, model training, evaluation, and export for deployment — is documented in `apple-training-testing.ipynb`.

## Team Members

- [	IKIP, SCIENTIST EGONG	23/EG/CO/027] – 
- [SENDAN, ABASIOFON UDUAK	23/EG/CO/087] – 
- [	JACK, BARISERE LEKARA	23/EG/CO/047] – 
- [	MICHAEL SAMUEL	23/EG/CO/127] – 
- [	UDO, MFONISO EMMANUEL	24/EG/CO/387] –   

## Project Objectives

- Source and merge apple images from multiple public datasets to build a larger, more diverse training set.
- Explore and clean the data, keeping only the classes relevant to this problem (Fresh, Formalin-mixed).
- Train and compare multiple deep learning approaches: a custom CNN built from scratch and a transfer-learning model based on MobileNetV3Small.
- Evaluate each model with standard classification metrics (accuracy, precision, recall, F1-score) and a confusion matrix.
- Package the best-performing model into a simple, accessible Streamlit application for real-time predictions.

## Features

- Binary image classification: **Fresh** vs **Formalin-mixed** apples.
- Two model architectures trained and compared:
  - A custom CNN (3 convolutional blocks with batch normalization and max pooling).
  - A MobileNetV3Small transfer-learning model, first trained with a frozen backbone (feature extraction) and then fine-tuned.
- Data augmentation (random flip, rotation, zoom) applied during training to improve generalization.
- Automated experiment tracking: training history, metrics, and model checkpoints are saved as JSON/PNG artifacts.
- Classification report and confusion matrix generation for objective model evaluation.
- Sample and misclassified prediction visualizations for qualitative error analysis.
- Simple Streamlit interface for uploading an apple image and getting a prediction with a confidence score.

## Technologies Used

- **Python 3**
- **TensorFlow / Keras** – model building, training, and MobileNetV3Small transfer learning
- **NumPy / Pandas** – data handling and analysis
- **Matplotlib / Seaborn** – visualizations (class distribution, learning curves, confusion matrix)
- **scikit-learn** – classification report, confusion matrix, evaluation metrics
- **Pillow (PIL)** – image loading and preprocessing
- **Hugging Face `datasets`** – loading the FruitVision Quality Classification dataset
- **Streamlit** – web app deployment
- **Jupyter Notebook** – experimentation and documentation

## Project Structure

```
apple-quality-ai-detectorn/
├── notebook/
    └──apple-training-testing.ipynb
    └──data-processing.ipynb   # Data prep, EDA, model training & evaluation
├── api/
    └──main.py                        # Streamlit web application
├── requirements.txt                # Python dependencies
├── models/
│   └── apple_quality_detector.keras
    └── apple_quality_tl_finetuned_best.keras
    └── apple_quality_cnn_best (1).keras
    └── best_apple_cnn.keras  # Exported model used by the Streamlit app

├── results/

└── README.md
```

> Note: adjust this tree to match your actual repository layout if it differs.

## Installation
```
git clone <repository-url>

cd Apple-Formalin-Detection

python -m venv .venv

# Activate the environment
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Usage

**Run the notebook** (optional, to retrain or inspect the pipeline):
```
jupyter notebook apple-training-testing.ipynb
```

**Run the Streamlit app locally:**
```
streamlit run main.py
```

Then open the local URL shown in the terminal (typically `http://localhost:8501`), upload an image of an apple, and view the predicted class (Fresh or Formalin-mixed) along with the model's confidence score.

**Live demo:** [add your deployed Streamlit app URL here]

## Model Performance

Three models were trained and evaluated on a held-out test set (952 images: 690 Fresh, 262 Formalin-mixed):

| Model | Test Accuracy | Test Precision | Test Recall | Test F1-Score |
|---|---|---|---|---|
| Custom CNN | 98.42% | 99.71% | 98.12% | 98.43% |
| Transfer Learning (frozen MobileNetV3Small) | 85.61% | 90.48% | 89.57% | — |
| Fine-Tuned Transfer Learning (MobileNetV3Small) | 87.92% | 93.76% | 89.28% | 91.46% |

The dataset used for training was built by merging and filtering two public sources — the Kaggle "Fresh, Rotten and Formalin-Mixed Fruit Detection" dataset and the Hugging Face "FruitVision Quality Classification" dataset — down to only the Apple images in the Fresh and Formalin-mixed classes, resulting in 9,494 images split 80/10/10 into training, validation, and test sets.



## Future Improvements

- Expand the dataset with more diverse lighting conditions, apple varieties, and camera angles to improve real-world robustness.
- Add a "Rotten" class back in for full three-way quality classification instead of a binary problem.
- Experiment with additional backbones (EfficientNet, ResNet) and compare against MobileNetV3Small.
- Add model explainability (e.g., Grad-CAM) so users can see which regions of the apple influenced the prediction.
- Optimize the model for mobile/edge deployment (TensorFlow Lite) for offline, in-field use.
- Add batch image upload support and a downloadable prediction report in the Streamlit app.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.