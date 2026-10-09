export function convertToArabicNumbers(number) {
  const arabicNumbers = ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"];
  // console.log(number);
  if (number?.includes("-")) {
    var number = number.split("-").reverse().join("-");
  }
  // console.log(number.replace(/\d/g, (digit) => arabicNumbers[digit]));

  return number.replace(/\d/g, (digit) => arabicNumbers[digit]);
}
