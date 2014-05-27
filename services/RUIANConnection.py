__author__ = 'Augustyn'

if (True):
    from RUIANReferenceDB import _findAddress, _getNearbyLocalities, _validateAddress, _findID
else:
    from postgisdb import _findAddress, _getNearbyLocalities, _validateAddress, _findID


findAddress = _findAddress
getNearbyLocalities = _getNearbyLocalities
validateAddress = _validateAddress
findID = _findID

