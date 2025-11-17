



Layer (type)	Output Shape	Number of Params	Connected to
InputLayer	(None, 34)	0	
Embedding Layer	(None, 34, 300)	17320500	InputLayer
Reshape	(None, 34, 300, 1)	0	Embedding Layer
Conv2D Block 1	(None, 34, 1, 512)	154112	Reshape
MaxPooling2D Block 1	(None, 1, 1, 512)	0	Conv2D Block 1
Conv2D Block 2	(None, 33, 1, 512)	307712	Reshape
MaxPooling2D Block 2	(None, 1, 1, 512)	0	Conv2D Block 2
Conv2D Block 3	(None, 32, 1, 512)	461312	Reshape
MaxPooling2D Block 3	(None, 1, 1, 512)	0	Conv2D Block 2
Conv2D Block 4	(None, 31, 1, 512)	614912	Reshape
MaxPooling2D Block 4	(None, 1, 1, 512)	0	Conv2D Block 2
Conv2D Block 5	(None, 30, 1, 512)	768512	Reshape
MaxPooling2D Block 5	(None, 1, 1, 512)	0	Conv2D Block 2
Conv2D Block 6	(None, 29, 1, 512)	922112	Reshape
MaxPooling2D Block 6	(None, 1, 1, 512)	0	Conv2D Block 2
Concatenate	(None, 6, 1, 512)	0	All MaxPooling2D Blocks
Flatten	(None, 3072)	0	Concatenate
Dropout Layer	(None, 3072)	0	Flatten
Dense Layer	(None, 27)	8297	Dropout Layer
This architecture contains total 20,632,143 trainable parameters.