## Chest Xray image Pneumonia prediction Example

This example shows how we can build pipeline to predict Pneumonia disease form chest Xray image.

We use a VIT based image classification model for inference. 

A key component of this demo is `XrayImageProcessor`, which is implemented based on huggingface pre-trained models. In this demo, we use [nickmuchi/vit-base-xray-pneumonia](https://huggingface.co/nickmuchi/vit-base-xray-pneumonia). You can use other pre-trained models by changing the `model_name` config.



## Run Example
You can run the following command to print the predictions for the images in the input folder path.

```bash
python chest_xray_image_classification.py input_path

# Examples: 

python chest_xray_image_classification.py sample_data

The meaning of arguments:

- `input_path`: the path of the input folder containing the xray images.

# the output will be the image file name followed by the probablity score of each class, displayed below.


sample_data/pneumonia_xray_image.jpeg
{'PNEUMONIA': 0.9714267253875732, 'NORMAL': 0.02857324108481407}

sample_data/normal_xray_image.jpeg
{'NORMAL': 0.9815188646316528, 'PNEUMONIA': 0.018481146544218063}