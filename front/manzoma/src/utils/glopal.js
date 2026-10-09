export function convertToArabicNumbers(number) {
  if (number === null || number === undefined) return number

  // Convert to string
  const numStr = String(number)

  const arabicNumbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']

  // Handle negative numbers (with "-")
  const processedStr = numStr.includes('-') ? numStr.split('-').reverse().join(' - ') : numStr

  // Replace digits with Arabic numbers
  return processedStr.replace(/\d/g, (digit) => arabicNumbers[digit])
}

export function getWsUrl(path) {
  const base = import.meta.env.VITE_MEDIA_BASE_URL
  console.log(base)
  console.log(path)
  return `${base}${path}`
}
