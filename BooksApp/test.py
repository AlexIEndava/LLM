from backend.services.llm_client import generate_and_save_image

prompt = "A creative book cover for ElonMusk: Tesla, SpaceX, and the Quest for a Fantastic Future"
filename = "backend/data/book_images/spacex1.png"
generate_and_save_image(prompt, filename)