import qrcode
from spire.pdf.common import *
from spire.pdf import *
from spire.pdf.security import *
from datetime import datetime


def sign_pdf(input_pdf, output_pdf, pfx_path, pfx_password, signer_name, signature_name):

    # ==========================
    # Data tanda tangan
    # ==========================
    name = signer_name
    contact = "Ttd Berjenjang System"
    location = "Kantor Cabang"
    reason = f"Ditandatangani oleh {signer_name}"
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data_to_sign = (
        f"Signed by: {name}; "
        f"Location: {location}; "
        f"Date: {date_time}; "
        f"Reason: {reason}"
    )

    # ==========================
    # Buat QR Code
    # ==========================
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=4,
        border=2
    )
    qr.add_data(data_to_sign)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("SigImg.png")

    # ==========================
    # Load PDF
    # ==========================
    doc = PdfDocument()
    doc.LoadFromFile(input_pdf)

    # ==========================
    # Load Sertifikat (PFX)
    # ==========================
    signatureMaker = PdfOrdinarySignatureMaker(doc, pfx_path, pfx_password)

    signature = signatureMaker.Signature
    signature.Name = name
    signature.ContactInfo = contact
    signature.Location = location
    signature.Reason = reason

    # ==========================
    # Appearance
    # ==========================
    appearance = PdfSignatureAppearance(signature)
    appearance.SignatureImage = PdfImage.FromFile("SigImg.png")
    appearance.GraphicMode = GraphicMode.SignImageAndSignDetail
    appearance.SignImageLayout = SignImageLayout.none

    # ==========================
    # Tentukan posisi per jabatan
    # ==========================
    positions = {
        "Manager": (80, 590),       # kiri
        "Supervisor": (220, 590),   # tengah
        "Staff": (360, 590),        # kanan
    }

    posX, posY = positions.get(signer_name, (80, 590))

    # ==========================
    # Tambah TTD
    # ==========================
    page = doc.Pages[0]

    signatureMaker.MakeSignature(
        signature_name,
        page,
        float(posX),
        float(posY),
        100.0,
        100.0,
        appearance
    )

    # ==========================
    # Save + Close
    # ==========================
    doc.SaveToFile(output_pdf)
    doc.Close()
    del doc
