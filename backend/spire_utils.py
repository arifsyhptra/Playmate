import qrcode
from spire.pdf.common import *
from spire.pdf import *
from datetime import datetime

def sign_pdf(input_pdf, output_pdf):
    # =======================
    # Data tanda tangan
    # =======================
    name = "Arief"
    contact = "+62 812345678"
    location = "DIPO SM Raja"
    reason = "I am the author."
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data_to_sign = (
        f"Name: {name}; Contact: {contact}; Location: {location}; "
        f"Date: {date_time}; Reason: {reason}"
    )

    # =======================
    # Buat QR code
    # =======================
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=4,     # kecil
        border=2        # tipis
    )
    qr.add_data(data_to_sign)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("SigImg.png")
    print("QR Code berhasil dibuat: SigImg.png")

    # =======================
    # Load PDF
    # =======================
    doc = PdfDocument()
    doc.LoadFromFile(input_pdf)

    # =======================
    # Load sertifikat digital (Gary.pfx)
    # =======================
    signatureMaker = PdfOrdinarySignatureMaker(doc, "gary.pfx", "e-iceblue")

    signature = signatureMaker.Signature
    signature.Name = name
    signature.ContactInfo = contact
    signature.Location = location
    signature.Reason = reason

    # =======================
    # QR + detail tanda tangan
    # =======================
    appearance = PdfSignatureAppearance(signature)
    appearance.SignatureImage = PdfImage.FromFile("SigImg.png")
    appearance.GraphicMode = GraphicMode.SignImageAndSignDetail
    appearance.SignImageLayout = SignImageLayout.none

    # =======================
    # Tambah ke halaman pertama
    # =======================
    page = doc.Pages[0]

    signatureMaker.MakeSignature(
        "Signature by Arief",
        page,
        90.0,   # X
        590.0,  # Y
        100.0,  # width
        100.0,  # height
        appearance
    )

    # =======================
    # Save
    # =======================
    doc.SaveToFile(output_pdf)
    doc.Close()

    print("PDF berhasil ditandatangani:", output_pdf)

# ===================================================
# Contoh pemanggilan
# ===================================================
sign_pdf("Sample.pdf", "Signed_with_QR_small.pdf")
