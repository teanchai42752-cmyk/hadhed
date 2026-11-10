/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: { fontFamily: { sans: ['Manrope', 'sans-serif'], mono: ['DM Mono', 'monospace'] }, colors: { ink: '#090d16', panel: '#111827', line: '#243044', mint: '#6ee7b7' } } },
  plugins: [],
}