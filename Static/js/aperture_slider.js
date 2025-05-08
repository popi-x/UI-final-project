console.log("✅ aperture_slider.js loaded");

document.addEventListener("DOMContentLoaded", function () {
  if (window.questionId !== 3) return;

  const apertureValues = window.apertureValues || [];
  console.log("📸 Aperture values:", apertureValues);

  const slider = document.getElementById("aperture-slider");
  const label = document.getElementById("aperture-value");

  if (!slider || !label || apertureValues.length === 0) {
    console.warn("🚫 Slider or label not found or values empty");
    return;
  }

  label.textContent = apertureValues[parseInt(slider.value)];

  slider.addEventListener("input", function () {
    const idx = parseInt(this.value);
    label.textContent = apertureValues[idx];
    console.log("🔁 Slider moved to:", idx, apertureValues[idx]);
  });

  console.log("🔎 label:", document.getElementById("aperture-value"));
  console.log("🔎 slider:", document.getElementById("aperture-slider"));

});
