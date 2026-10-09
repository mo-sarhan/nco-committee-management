import html2canvas from 'html2canvas'
// import { jsPDF } from "jspdf"

export function useImageUtils() {
  // Note: window.jspdf needs to be available globally (e.g., loaded via <script> tag or installed)
  const downloadPDF = async (milNo) => {
    const element = document.getElementById('capture-area')
    if (!element) return

    const canvas = await html2canvas(element, { scale: 2 })
    const imgData = canvas.toDataURL('image/png')

    const { jsPDF } = window.jspdf
    const pdf = new jsPDF({
      orientation: 'l',
      unit: 'mm',
      format: 'a4',
    })

    const imgProps = pdf.getImageProperties(imgData)
    const pdfWidth = pdf.internal.pageSize.getWidth()
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width

    pdf.addImage(imgData, 'PNG', 0, 15, pdfWidth, pdfHeight + 45)
    pdf.save(`${milNo}.pdf`)
  }

  const downloadImage = async (milNo) => {
    const element = document.getElementById('capture-area')
    if (!element) return

    const canvas = await html2canvas(element)
    const image = canvas.toDataURL('image/png')

    const link = document.createElement('a')
    link.href = image
    link.download = `${milNo}.png`
    link.click()
  }

  return { downloadPDF, downloadImage }
}
