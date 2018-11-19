# plivoassignment
Design A phonebook

To run :
python api.py

sample request to add contact:
    curl -X PUT \
  http://localhost:8000/plivo/v1/createphonebook \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: b6021cd5-29b3-402e-98a2-b2333c67b03f' \
  -H 'cache-control: no-cache' \
  -d '{
	"email":"abcb@artifacia.com",
	"number":999999999,
	"name":"Ashish"
}'

sample request to delete contact:
    curl -X DELETE \
  http://localhost:8000/plivo/v1/deletecontact \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 68f1ad23-a581-4029-8af7-b49e0e7df4d6' \
  -H 'cache-control: no-cache' \
  -d '{
	"number":"999000099999"
}'


sample request to update contact:
    curl -X POST \
  http://localhost:8000/plivo/v1/editcontact \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: ac0c1efd-5269-4d26-a3e0-e457749cb4d3' \
  -H 'cache-control: no-cache' \
  -d '{
	"number":999999999,
	"data_tobe_updated":{"name":"Dinesh"}
}'

sample request to search contact:
    curl -X GET \
  'http://localhost:8000/plivo/v1/searchcontact?start=0&email=abcb@artifacia.com%20' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 84f42d6e-363e-4e65-85e7-bc3dfbedfbb9' \
  -H 'cache-control: no-cache'
