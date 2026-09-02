import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import export_to_video, load_image
import os

print("Starte vollständigen Download und Initialisierung der Film-KI...")

# Modell-ID für Stable Video Diffusion
model_id = "stabilityai/stable-video-diffusion-img2vid-xt"

print("Lade Modell-Gewichte herunter (dies kann einige Minuten dauern)...")
pipeline = StableVideoDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float32,
    variant="fp16" if torch.cuda.is_available() else None
)

if torch.cuda.is_available():
    pipeline.enable_model_cpu_offload()
    print("CUDA-Beschleunigung aktiviert.")
else:
    print("Keine GPU gefunden, Ausführung läuft auf der CPU (sehr langsam).")

print("Lade Test-Bild für die Generierung...")
image = load_image("https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/svd/rocket.png")
image = image.resize((512, 512)) # Reduzierte Auflösung für Stabilität

print("Generiere Frames...")
frames = pipeline(image, decode_chunk_size=2, generator=torch.manual_seed(42)).frames[0]

print("Speichere finalen Film-Clip...")
export_to_video(frames, "generated_scene.mp4", fps=7)
print("Alle Komponenten erfolgreich heruntergeladen und Film erstellt!")
