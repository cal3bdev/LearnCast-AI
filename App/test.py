import asyncio
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key="sk-proj-S4LvJgAHOwycFE9F61LfT3BlbkFJCor3dat5NLg3aufGEMlH")


input = "Absolutely! Transient circuits are essentially circuits that change over time, specifically because of sudden changes like closing a switch. So, imagine you have a car, right? When you start accelerating, there's a moment of inertia—the car doesn’t just zoom off immediately. Similarly, transient analysis looks at how current and voltage respond immediately after a switch is closed, then how they settle into a steady state over time"
 
async def test():
    response = await client.audio.speech.create(
    model="tts-1",
    voice="shimmer",
    input=input,
)

    response.stream_to_file("output2.mp3")
    return f"output.mp3"

asyncio.run(test())

