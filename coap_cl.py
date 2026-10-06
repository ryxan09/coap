import asyncio
from aiocoap import Context, Message
from aiocoap.numbers.codes import Code


SERVER = "coap://127.0.0.1:5683/temperature"


async def request(method, payload=None):

    protocol = await Context.create_client_context()

    request = Message(
        code=method,
        uri=SERVER
    )

    if payload:
        request.payload = payload.encode("utf-8")

    response = await protocol.request(request).response

    print()
    print("Response:", response.payload.decode())
    print()


async def main():

    while True:

        print("========================================")
        print("           CoAP TEMPERATURE CLIENT")
        print("========================================")
        print("1. GET temperature")
        print("2. POST city")
        print("3. PUT city")
        print("4. DELETE city")
        print("5. Exit")
        print()

        choice = input("Choose an operation: ")

        if choice == "1":

            await request(1)

        elif choice == "2":

            city = input("Enter city: ")

            await request(
                2,
                city
            )

        elif choice == "3":

            city = input("Enter city: ")

            await request(
                3,
                city
            )

        elif choice == "4":

            await request(4)

        elif choice == "5":

            break

        else:

            print("Invalid choice.")


if __name__ == "__main__":
    asyncio.run(main())