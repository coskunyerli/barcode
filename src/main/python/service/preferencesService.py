from model.preferences import ObjectDict

_preferences = ObjectDict()


class PreferencesService(object):
	def preferences(self):
		return _preferences