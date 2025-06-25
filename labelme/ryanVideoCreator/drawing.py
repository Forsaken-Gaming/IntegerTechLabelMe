import cv2

def draw_rectangle_with_label(image, shape, filename, metrics=None):
   
    points = shape['points']
    top_left = tuple(map(int, points[0])) 
    bottom_right = tuple(map(int, points[1])) 
    label_position = (top_left[0], top_left[1] - 10)
    label_name = shape['label']

    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
    cv2.putText(image, label_name, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    if metrics != None:
        midpoint = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        cv2.circle(image, midpoint, 5, (0, 0, 255), -1)  # Draw a red dot at the midpoint
        metrics.flagInvalidLabel(filename, label_name)
    # return midpoint


def draw_filename(image, filename, text_position_offset=100):
   
    text_position = (image.shape[1] // 2 - text_position_offset, image.shape[0] - 10)
    cv2.putText(image, filename, text_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 2, cv2.LINE_AA)

def draw_annotations_on_image(image, annotations, filename, text_position_offset=100, metrics=None):
    '''
    return:
        2-tuple: (image, number of labels on image)
    '''
    if annotations:
        for shape in annotations.get('shapes', []):
            if shape['shape_type'] == 'rectangle':
                draw_rectangle_with_label(image, shape, filename, metrics)
    draw_filename(image, filename, text_position_offset)
    label_count = len(annotations.get('shapes', [])) if annotations else 0
    return (image, label_count)
