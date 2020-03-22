import PySide2.QtWidgets as QtWidgets, PySide2.QtGui as QtGui, PySide2.QtCore as QtCore


class SearchSoldProductDelegate(QtWidgets.QStyledItemDelegate):
	def paint(self, painter, option, index):
		order = index.data(QtCore.Qt.UserRole)
		rect = option.rect
		isSelected = option.state & QtWidgets.QStyle.State_Selected
		if isSelected:
			painter.fillRect(rect, QtGui.QColor('#303030'))
		soldProductList = list(map(lambda soldProduct: soldProduct.name(), order.committedProductList[:6]))

		painter.save()
		painter.setPen(QtGui.QColor('#aaaaaa'))
		font = painter.font()
		font.setPointSize(11)
		painter.setFont(font)
		date = order.createdDate().strftime("%m-%d-%Y")
		fontMetrics = painter.fontMetrics()
		dateWidth = fontMetrics.width(date)
		painter.drawText(QtCore.QRect(rect.right() - dateWidth - 8, rect.top() + 2, dateWidth, fontMetrics.height()),
						 QtCore.Qt.AlignCenter, date)

		length = f'({len(order.committedProductList)})'
		lengthWidth = fontMetrics.width(length)
		painter.drawText(
				QtCore.QRect(rect.right() - lengthWidth - 8, rect.bottom() - fontMetrics.height() - 2, lengthWidth,
							 fontMetrics.height()), QtCore.Qt.AlignCenter, length)

		painter.restore()
		# ElideRight
		productListStringRect = QtCore.QRect(rect.left() + 8, rect.top(), rect.width() - dateWidth - 8, rect.height())
		productListString = fontMetrics.elidedText(
				', '.join(soldProductList), QtCore.Qt.ElideRight, productListStringRect.width())
		painter.drawText(productListStringRect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, productListString)
		painter.fillRect(QtCore.QRect(rect.left(), rect.bottom(), rect.width(), 1), QtGui.QColor('#303030'))


	def sizeHint(self, option, index):
		return QtCore.QSize(100, 40)
