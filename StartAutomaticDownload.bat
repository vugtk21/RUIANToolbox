echo "Startuji službu pro automatické stahování a import dat RÚIAN"
echo "============================================================"
cd RUIANDownloader
python.exe windowsservice.py install
NET START RUIANDld