#Öğrenme Notu
Bu proje, MQTT broker'ın nasıl çalıştığını, backend'in bir sensörden gelen veriyi nasıl işlediğini ve bir API'nin nasıl yazıldığını uçtan uca ilk kez uyguladığım öğrenme projemdir. Aşağıda ezbelemek açısından rahat etmek için bazı terminal kodlarını ekledim:

#Terminal Kodları
.venv açmak için:
.venv\Scripts\activate

API açmak için:
uvicorn api.main:app --reload
 
--windows--
py run_backend.py
py main.py

--linux--
python run_backend.py
python main.py

--Endpointler--
http://127.0.0.1:8000/devices
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/metrics
http://127.0.0.1:8000/metrics/latest
http://127.0.0.1:8000/dashboard
