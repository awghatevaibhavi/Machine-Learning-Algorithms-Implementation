import csv
def main():
	input_file = []
	#reading the validation file
	with open('HW_05B_DecTree_validation_data___v200.csv') as csvfile:
		attributes = csv.reader(csvfile)
		for element in attributes:
			input_file.append(','.join(element))
	for index in range( len(input_file)):
		input_file[index] = input_file[index].split(',')
	for row in range(1, len(input_file)):
		for col in range(0,4):
			input_file[row][col] = float(input_file[row][col])
	input_file.pop(0)
	#writing the classifications to output file as per the decision tree
	with open('HW_05B_Awghate_Vaibhavi_MyClassifications.csv','w',newline='') as csvfile1:
		csvwriter = csv.writer(csvfile1)
		for row in range(0, len(input_file)):
			if input_file[row][1]  > 8.010000 :
				csvwriter.writerow('0')
			else:
				if input_file[row][3]  > 5.080000 :
					if input_file[row][1]  > 5.060000 :
						csvwriter.writerow('1')
					else:
						csvwriter.writerow('0')
				else:
					csvwriter.writerow('1')
main()