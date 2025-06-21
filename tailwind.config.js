/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Path to Django templates
    './**/templates/**/*.html', // If you have multiple apps
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Roboto', 'sans-serif'], // Add Roboto as the default sans font
      },
    },
  },
  plugins: [],
};


