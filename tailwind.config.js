/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    fontFamily: {
      sans: ["IBM Plex Sans Thai", "sans-serif"],
    },
    extend: {
      colors: {
        primary: {
          DEFAULT: "#CF893F",
          50: "#F4E3D2",
          100: "#F0D9C2",
          200: "#E7C5A1",
          300: "#DFB180",
          400: "#D79D60",
          500: "#CF893F",
          600: "#AB6D2B",
          700: "#7E5020",
          800: "#513414",
          900: "#241709",
          950: "#0E0904",
        },
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
