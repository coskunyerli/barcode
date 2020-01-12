def _binarySearch(arr, l, r, cmp):
	# Check base case
	if r >= l:
		mid = int(l + (r - l) / 2)
		res = cmp(arr[mid])
		# If element is present at the middle itself
		if res == 0:
			return mid

		# If element is smaller than mid, then it
		# can only be present in left subarray
		elif res > 0:
			return _binarySearch(arr, l, mid - 1, cmp)

		# Else the element can only be present
		# in right subarray
		else:
			return _binarySearch(arr, mid + 1, r, cmp)

	else:
		# Element is not present in the array
		return None


def binarySearch(arr, cmp):
	return _binarySearch(arr, 0, len(arr) - 1, cmp)


def cmp(a, b):
	return (a > b) - (a < b)


def openQss(filename):
	try:
		f = open(filename)
		style = f.read()
	except:
		style = ''

	return style


def first_(func, arr):
	for item in arr:
		if func(item):
			return item
	return None
