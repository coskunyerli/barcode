import os

from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PySide2 import ApplicationContext


class BarcodeApplicationContext(ApplicationContext):
	@cached_property
	def app(self):
		result = self._qt_binding.QApplication([])
		result.setApplicationName(self.build_settings['app_name'])
		result.setApplicationVersion(self.build_settings['version'])
		return result


	def qss(self, filename):
		try:
			with open(self.get_resource(os.path.join('qss', filename))) as file:
				qssString = file.read()
				return qssString
		except Exception as e:
			return None
