import pushbullet
import requests
import uuid
import logging

if __name__ == '__main__':
  logging.basicConfig(filename='/var/log/vaccine/runs.log', format='%(asctime)s %(message)s', level=logging.INFO)
  r = requests.get("https://partners.doctolib.fr/booking/centre-de-vaccination-covid-de-versailles.json")
  new_update = r.text
  with open("./update.json", "r") as f:
    old_update = f.read()
  if old_update == new_update:
    print("same")
    logging.info("Ran with no change")
  else:
    print("different")
    with open("./update.json", "w") as f:
      f.write(new_update)
      f.close()
    uuidstr = str(uuid.uuid4()).upper()[:8]
    with open(f"./updates/old_update_{uuidstr}.json", "w") as f:
      f.write(old_update)
      f.close()
    pb = pushbullet.Pushbullet("o.rEeCCbOt5Lgu1Mf9g466AlfhBsUDOcwe")
    dev = pb.devices[0]
    dev.push_note("Alert!", "A change was detected! Visit https://partners.doctolib.fr/centre-de-sante/versailles/centre-de-vaccination-covid-de-versailles?speciality_id=5494")
    logging.info("Ran with changes")
    logging.info(new_update)
