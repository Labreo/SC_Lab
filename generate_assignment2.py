import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import subprocess
import os
import shutil

DOCX_OUT_LAB = '/Users/sanjaywaradkar/SC_Lab/SC_Assignment_2_Kanak_Waradkar.docx'
DOCX_OUT_DOWN = '/Users/sanjaywaradkar/Downloads/SC_Assignment_2_Kanak_Waradkar.docx'
PDF_OUT_LAB = '/Users/sanjaywaradkar/SC_Lab/SC_Assignment_2_Kanak_Waradkar.pdf'
PDF_OUT_DOWN = '/Users/sanjaywaradkar/Downloads/SC_Assignment_2_Kanak_Waradkar.pdf'
FIG_DIR = '/Users/sanjaywaradkar/SC_Lab/figures'

C_NAVY = RGBColor(26, 54, 93)      # #1A365D - Main Headings
C_BLUE = RGBColor(43, 108, 176)    # #2B6CB0 - Subheadings
C_DARK = RGBColor(45, 55, 72)      # #2D3748 - Body Text
C_MUTED = RGBColor(113, 128, 150)  # #718096 - Metadata / Footnotes
C_RED = RGBColor(197, 48, 48)      # #C53030 - Highlights

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def add_header_card(doc):
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("GOA COLLEGE OF ENGINEERING")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(15)
    r_inst.font.bold = True
    r_inst.font.color.rgb = C_NAVY

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(0)
    p_dept.paragraph_format.space_after = Pt(2)
    r_dept = p_dept.add_run("DEPARTMENT OF COMPUTER ENGINEERING | FARMAGUDI, PONDA - GOA")
    r_dept.font.name = "Arial"
    r_dept.font.size = Pt(9.5)
    r_dept.font.bold = True
    r_dept.font.color.rgb = C_MUTED

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_before = Pt(2)
    p_course.paragraph_format.space_after = Pt(6)
    r_course = p_course.add_run("Course: Soft Computing (CMP-325) • Semester V (2026–2027)")
    r_course.font.name = "Arial"
    r_course.font.size = Pt(10.5)
    r_course.font.bold = True
    r_course.font.color.rgb = C_BLUE

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("ASSIGNMENT - II: SOLUTIONS & COMPREHENSIVE ANALYSIS")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(13)
    r_title.font.bold = True
    r_title.font.color.rgb = C_NAVY

    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="CBD5E0", sz="6", val="single")

    meta = [
        [("Name of Student:", " Kanak Sanjay Waradkar"), ("Roll Number:", " 24B-0CO-030")],
        [("Class & Batch:", " Third Year Computer Engg. (Batch C)"), ("Subject:", " Soft Computing (CMP-325)")]
    ]

    for row_idx, row_data in enumerate(meta):
        row = table.rows[row_idx]
        make_row_cant_split(row)
        for col_idx, (k, v) in enumerate(row_data):
            cell = row.cells[col_idx]
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            set_cell_shading(cell, "F7FAFC" if row_idx % 2 == 0 else "EDF2F7")
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            rk = p.add_run(k)
            rk.font.name = "Arial"
            rk.font.size = Pt(9.5)
            rk.font.bold = True
            rk.font.color.rgb = C_NAVY

            rv = p.add_run(v)
            rv.font.name = "Arial"
            rv.font.size = Pt(9.5)
            rv.font.bold = True if ("Kanak" in v or "24B" in v or "Batch C" in v) else False
            rv.font.color.rgb = C_DARK

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(6)
    p_sp.paragraph_format.space_after = Pt(6)

def add_question_box(doc, q_num, q_title):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    make_row_cant_split(tbl.rows[0])
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    set_cell_shading(cell, "EBF8FF")

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="2B6CB0"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    
    r_num = p.add_run(f"Question {q_num}: ")
    r_num.font.name = "Arial"
    r_num.font.size = Pt(10.5)
    r_num.font.bold = True
    r_num.font.color.rgb = C_BLUE

    r_txt = p.add_run(q_title)
    r_txt.font.name = "Arial"
    r_txt.font.size = Pt(10.5)
    r_txt.font.bold = True
    r_txt.font.color.rgb = C_NAVY

    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_before = Pt(2)
    p_post.paragraph_format.space_after = Pt(2)
    p_post.paragraph_format.keep_with_next = True

def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8 if level == 1 else 6)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(11 if level == 1 else 10)
    r.font.bold = True
    r.font.color.rgb = C_NAVY if level == 1 else C_BLUE

def add_para(doc, text, bold_prefix="", italic_prefix="", bullet=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3.5)
    p.paragraph_format.line_spacing = 1.15
    if bullet:
        p.paragraph_format.left_indent = Inches(0.25)
        r_bullet = p.add_run("• ")
        r_bullet.font.name = "Arial"
        r_bullet.font.size = Pt(9.5)
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = C_BLUE

    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = "Arial"
        r_b.font.size = Pt(9.5)
        r_b.font.bold = True
        r_b.font.color.rgb = C_DARK

    if italic_prefix:
        r_i = p.add_run(italic_prefix)
        r_i.font.name = "Arial"
        r_i.font.size = Pt(9.5)
        r_i.font.italic = True
        r_i.font.color.rgb = C_DARK

    r_txt = p.add_run(text)
    r_txt.font.name = "Arial"
    r_txt.font.size = Pt(9.5)
    r_txt.font.color.rgb = C_DARK

def add_callout(doc, formula_text, caption=""):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    make_row_cant_split(tbl.rows[0])
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=60, bottom=60, left=120, right=120)
    set_cell_shading(cell, "F7FAFC")

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/>'
        f'<w:left w:val="single" w:sz="16" w:space="0" w:color="4299E1"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True

    rf = p.add_run(formula_text)
    rf.font.name = "Arial"
    rf.font.size = Pt(9.5)
    rf.font.bold = True
    rf.font.color.rgb = C_NAVY

    if caption:
        p_cap = cell.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(2)
        rc = p_cap.add_run(caption)
        rc.font.name = "Arial"
        rc.font.size = Pt(8.5)
        rc.font.italic = True
        rc.font.color.rgb = C_MUTED

    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_before = Pt(2)
    p_post.paragraph_format.space_after = Pt(2)

def add_table_custom(doc, headers, data, col_widths=None):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl, color="CBD5E0", sz="4", val="single")

    hdr_row = tbl.rows[0]
    make_row_cant_split(hdr_row)
    hdr_cells = hdr_row.cells
    for i, title in enumerate(headers):
        cell = hdr_cells[i]
        set_cell_margins(cell, top=80, bottom=80, left=90, right=90)
        set_cell_shading(cell, "1A365D")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(title)
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_values in enumerate(data):
        row = tbl.rows[r_idx + 1]
        make_row_cant_split(row)
        row_cells = row.cells
        bg_col = "F7FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = row_cells[c_idx]
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            set_cell_shading(cell, bg_col)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Arial"
            r.font.size = Pt(8.5)
            r.font.color.rgb = C_DARK

    if col_widths:
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    p_post = doc.add_paragraph()
    p_post.paragraph_format.space_before = Pt(3)
    p_post.paragraph_format.space_after = Pt(3)

def add_figure(doc, img_path, caption="", width=Inches(5.4)):
    if os.path.exists(img_path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run()
        run.add_picture(img_path, width=width)

        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(1)
            p_cap.paragraph_format.space_after = Pt(5)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Arial"
            r_cap.font.size = Pt(8.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = C_MUTED

def set_footer_and_header(doc):
    for s in doc.sections:
        s.top_margin = Inches(0.7)
        s.bottom_margin = Inches(0.7)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

        hdr = s.header
        p_hdr = hdr.paragraphs[0]
        p_hdr.text = "Soft Computing (CMP-325) | Assignment - II"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.runs[0].font.name = "Arial"
        p_hdr.runs[0].font.size = Pt(8.5)
        p_hdr.runs[0].font.color.rgb = C_MUTED

        ftr = s.footer
        p_ftr = ftr.paragraphs[0]
        p_ftr.text = "Kanak Sanjay Waradkar  |  Roll No: 24B-0CO-030  |  Batch C  |  Department of Computer Engineering, GEC"
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_ftr.runs[0].font.name = "Arial"
        p_ftr.runs[0].font.size = Pt(8)
        p_ftr.runs[0].font.color.rgb = C_MUTED

# ----------------- QUESTION BUILDERS -----------------

def build_q1(doc):
    add_question_box(doc, 1, "What are Autoencoders? Explain the working of various Autoencoders in brief.")
    add_heading(doc, "1. Introduction and Core Concepts of Autoencoders", level=1)
    add_para(doc, "An Autoencoder is a specialized class of unsupervised artificial neural network designed to learn efficient, compressed, and low-dimensional representations (latent encodings) of unlabeled input data by training the network to reproduce its input at its output layer. Rather than performing supervised target classification, an autoencoder operates under self-supervision, minimizing the discrepancy between the original input x and its reconstructed counterpart x̂.")
    
    add_para(doc, "An autoencoder fundamentally comprises three interconnected components:", bold_prefix="Architectural Components: ")
    add_para(doc, "Maps the high-dimensional input vector x ∈ ℝᴰ into a lower-dimensional latent representation z ∈ ℝᵈ (where d < D). Mathematically: z = f_θ(x) = σ(W_e x + b_e), where W_e is the encoder weight matrix, b_e is the bias vector, and σ is an activation function (e.g., ReLU, Sigmoid).", bold_prefix="1. Encoder (Recognition Network): ", bullet=True)
    add_para(doc, "The central bottleneck layer holding the compact representation z. This bottleneck prevents trivial identity mapping and forces the network to retain only the most critical, non-redundant statistical features.", bold_prefix="2. Bottleneck (Latent Space / Code): ", bullet=True)
    add_para(doc, "Reconstructs the original data from the compressed latent code z back into the original input space. Mathematically: x̂ = g_θ'(z) = σ'(W_d z + b_d), where W_d and b_d represent the decoder weight matrix and bias vector.", bold_prefix="3. Decoder (Generative Network): ", bullet=True)
    
    add_callout(doc, "Reconstruction Loss:  L(x, x̂) = (1 / 2) ||x - x̂||²   (MSE)   OR   L(x, x̂) = - Σ [ x_i log(x̂_i) + (1 - x_i) log(1 - x̂_i) ]", "Mean Squared Error (for continuous data) and Binary Cross-Entropy (for normalized inputs)")
    add_figure(doc, f"{FIG_DIR}/diagram_autoencoder.png", "Figure 1.1: Canonical Architecture of an Autoencoder showing Encoder, Bottleneck Latent Space, and Decoder.")

    add_heading(doc, "2. Working of Various Autoencoder Variants", level=1)
    add_para(doc, "To prevent autoencoders from simply memorizing the training set and to imbue the latent space with useful semantic properties, several autoencoder architectures have been developed:")
    
    add_para(doc, "The bottleneck layer has strictly smaller dimensionality than the input space (dim(z) < dim(x)). By imposing an information capacity constraint, it discovers the primary nonlinear manifold of the dataset, effectively acting as a nonlinear generalization of Principal Component Analysis (PCA).", bold_prefix="1. Undercomplete Autoencoder: ", bullet=True)
    add_para(doc, "The latent layer has equal or higher dimensionality than the input space (dim(z) ≥ dim(x)). Without regularization, an overcomplete network would trivially memorize an identity function. It must therefore be paired with regularization constraints such as sparsity or noise injection.", bold_prefix="2. Overcomplete Autoencoder: ", bullet=True)
    add_para(doc, "Imposes a sparsity penalty on the latent neuron activations, ensuring that for any given input, only a small fraction of latent neurons fire. This is mathematically achieved by adding Kullback-Leibler (KL) divergence between the mean activation ρ̂_j and a small target sparsity parameter ρ (e.g., ρ = 0.05) to the loss: L_sparse = L(x, x̂) + β Σ KL(ρ || ρ̂_j).", bold_prefix="3. Sparse Autoencoder (SAE): ", bullet=True)
    add_para(doc, "Instead of taking clean data, the input x is deliberately corrupted by adding stochastic noise (e.g., Gaussian noise or masking noise) to produce x̃. The autoencoder is trained to reconstruct the original, uncorrupted input x from the noisy input x̃. This forces the model to learn the underlying manifold topology and robustly project off-manifold points back onto the true data manifold.", bold_prefix="4. Denoising Autoencoder (DAE): ", bullet=True)
    add_para(doc, "Encourages the learned representation to be robust against infinitesimal input variations by adding an analytical regularizer: the Frobenius norm of the Jacobian matrix of encoder activations with respect to the input: L_CAE = L(x, x̂) + λ ||J_f(x)||_F². This penalizes sharp variations in the latent space along irrelevant directions while retaining manifold sensitivity.", bold_prefix="5. Contractive Autoencoder (CAE): ", bullet=True)
    add_para(doc, "A probabilistic, generative model where the encoder predicts the parameters of a probability distribution (mean vector μ and log-variance log(σ²)) in latent space. Latent vectors z are sampled using the reparameterization trick: z = μ + σ ⊙ ε (where ε ~ N(0, I)). The training objective maximizes the Evidence Lower Bound (ELBO), optimizing both reconstruction fidelity and KL divergence against a standard Gaussian prior: L_VAE = -E_q[log p(x|z)] + D_KL(q(z|x) || p(z)).", bold_prefix="6. Variational Autoencoder (VAE): ", bullet=True)
    add_para(doc, "Replaces fully connected layers with 2D convolutional and pooling layers in the encoder, and transposed convolutions (or upsampling) in the decoder. It preserves spatial 2D grid relationships and is the standard choice for image compression, feature extraction, and inpainting.", bold_prefix="7. Convolutional Autoencoder (CAE): ", bullet=True)

def build_q2(doc):
    doc.add_page_break()
    add_question_box(doc, 2, "Explain the characteristics and architecture of neuro-fuzzy hybrid system. List the advantages and disadvantages of this system.")
    add_heading(doc, "1. Characteristics of Neuro-Fuzzy Hybrid Systems", level=1)
    add_para(doc, "A Neuro-Fuzzy Hybrid System combines the complementary strengths of Artificial Neural Networks (ANNs) and Fuzzy Logic Systems (FLS). While ANNs excel at low-level numerical computation, pattern learning from raw empirical data, and self-adaptation, they operate as opaque 'black boxes'. Conversely, Fuzzy Logic systems provide transparent, interpretable 'white box' linguistic reasoning ('IF premise THEN consequent') but lack inherent mechanisms to learn or automatically tune membership functions from data. Neuro-fuzzy integration eliminates both shortcomings.")
    
    add_para(doc, "Key characteristics include:", bold_prefix="Salient Characteristics: ")
    add_para(doc, "Maintains linguistic interpretability through fuzzy IF-THEN rules while utilizing neural connection weights to encode fuzzy parameters.", bold_prefix="• Hybrid Knowledge Representation: ")
    add_para(doc, "Employs gradient-based or hybrid learning algorithms (e.g., backpropagation, least squares) to tune membership function shapes, centers, and rule consequents directly from input-output datasets.", bold_prefix="• Self-Learning and Adaptability: ")
    add_para(doc, "The fuzzy rule structure provides graceful degradation and robust tolerance when handling noisy, missing, or imprecise real-world inputs.", bold_prefix="• Fault and Uncertainty Tolerance: ")
    add_para(doc, "Can approximate any continuous real-valued nonlinear function on a compact domain to an arbitrary degree of accuracy.", bold_prefix="• Universal Function Approximation: ")

    add_heading(doc, "2. Architecture: Adaptive Neuro-Fuzzy Inference System (ANFIS)", level=1)
    add_para(doc, "The most prominent and widely adopted neuro-fuzzy architecture is ANFIS (Jang, 1993), which implements a first-order Takagi-Sugeno-Kang (TSK) fuzzy inference model structured across a 5-layer feedforward neural network:")
    add_figure(doc, f"{FIG_DIR}/diagram_neuro_fuzzy.png", "Figure 2.1: 5-Layer ANFIS Architecture with two inputs (x, y), two fuzzy rules, and a single overall output.")

    add_para(doc, "Mathematical layer-by-layer operation:", bold_prefix="ANFIS 5-Layer Formulation: ")
    add_para(doc, "Every node i in this layer is an adaptive node representing a linguistic label (e.g., Small, Large). The node output is the membership grade of the input x:  O_{1,i} = μ_{A_i}(x). For example, using a generalized Bell membership function: μ_{A_i}(x) = 1 / (1 + |(x - c_i) / a_i|^(2 b_i)), where {a_i, b_i, c_i} are the learnable premise parameters.", bold_prefix="• Layer 1 (Fuzzification Layer): ")
    add_para(doc, "Every node in this layer is a fixed node labeled Π. It computes the firing strength w_i of a rule by performing a fuzzy T-norm operation (product):  O_{2,i} = w_i = μ_{A_i}(x) × μ_{B_i}(y).", bold_prefix="• Layer 2 (Rule Firing Layer): ")
    add_para(doc, "Every node is a fixed node labeled N. It computes the normalized firing strength of the i-th rule relative to all rules:  O_{3,i} = w̄_i = w_i / (w_1 + w_2).", bold_prefix="• Layer 3 (Normalization Layer): ")
    add_para(doc, "Every node is an adaptive node computing the first-order polynomial consequent of the rule:  O_{4,i} = w̄_i f_i = w̄_i (p_i x + q_i y + r_i), where {p_i, q_i, r_i} are learnable consequent parameters.", bold_prefix="• Layer 4 (Consequent / Defuzzification Layer): ")
    add_para(doc, "A single fixed node labeled Σ that computes the overall crisp system output by summing the incoming signals:  O_{5,1} = y_{out} = Σ_i w̄_i f_i = (Σ w_i f_i) / (Σ w_i).", bold_prefix="• Layer 5 (Overall Output Layer): ")

    add_callout(doc, "Hybrid Learning Rule: Forward Pass uses Least Squares Estimation (LSE) for consequent parameters {p, q, r}; Backward Pass uses Gradient Descent (Backpropagation) for premise parameters {a, b, c}.", "ANFIS Hybrid Learning Paradigm")

    add_heading(doc, "3. Advantages and Disadvantages", level=1)
    headers = ["Aspect", "Advantages", "Disadvantages"]
    data = [
        ["Interpretability", "Transparent rule structure; human experts can inspect and validate the acquired fuzzy rules.", "Excessive rules or shifting membership functions can reduce linguistic readability."],
        ["Learning Speed", "Hybrid learning (LSE + Backprop) achieves extremely fast convergence compared to pure ANNs.", "Curse of dimensionality: number of rules grows exponentially with input variables (M^n rules)."],
        ["Prior Knowledge", "Can incorporate existing heuristic domain rules as initial network weights before training.", "Requires careful manual initialization of membership functions to prevent local minima."],
        ["Adaptability", "Continuously updates and fine-tunes parameters dynamically in changing environments.", "Computationally heavy forward-backward passes on large multidimensional datasets."]
    ]
    add_table_custom(doc, headers, data, [Inches(1.4), Inches(2.7), Inches(2.7)])

def build_q3(doc):
    doc.add_page_break()
    add_question_box(doc, 3, "Explain convolution operation in a CNN with block diagram and suitable example. List the applications of CNN.")
    add_heading(doc, "1. The Convolution Operation in CNN", level=1)
    add_para(doc, "The convolution operation is the foundational building block of Convolutional Neural Networks (CNNs). In mathematical terms, 2D discrete convolution operates on an input tensor (such as a 2D image feature map I) and a learnable parameter matrix known as a kernel or filter K. The filter slides across the spatial dimensions of the input, performing element-wise multiplications within its local receptive field and summing the products, optionally followed by an additive bias term b.")
    
    add_callout(doc, "S(i, j) = (I * K)(i, j) = Σ_m Σ_n I(i + m, j + n) K(m, n) + b", "Discrete 2D Cross-Correlation / Convolution Equation")
    
    add_para(doc, "CNNs leverage three vital architectural advantages over traditional fully connected networks:", bold_prefix="Key Principles: ")
    add_para(doc, "Each hidden unit connects only to a localized spatial region of the input rather than every input pixel, dramatically reducing weight parameters.", bold_prefix="1. Sparse Connectivity (Local Receptive Fields): ", bullet=True)
    add_para(doc, "The same filter weights are applied across all spatial locations of the feature map, embedding translational equivariance (an edge or pattern detected at the top-left is detected identically at the bottom-right).", bold_prefix="2. Parameter Sharing: ", bullet=True)
    add_para(doc, "Output spatial dimensions depend on input size W, kernel size F, zero-padding P, and stride S:  O = floor((W - F + 2P) / S) + 1.", bold_prefix="3. Spatial Output Formula: ", bullet=True)

    add_heading(doc, "2. Block Diagram and Fully Worked Numerical Example", level=1)
    add_figure(doc, f"{FIG_DIR}/diagram_cnn_conv.png", "Figure 3.1: 2D Convolution Operation sliding a 2x2 kernel across a 4x4 input to produce a 3x3 feature map.")

    add_para(doc, "Consider a 4x4 input feature map I, convolved with a 2x2 filter K, using stride S = 1 and zero padding P = 0:")
    add_callout(doc, "Input I = [ [2, 1, 0, 3],  [1, 3, 2, 1],  [0, 2, 1, 0],  [3, 1, 0, 2] ]\nKernel K = [ [1, 0],  [0, 1] ]     (Bias b = 0)", "Input Matrix and Convolution Filter")
    
    add_para(doc, "The output dimension is O = floor((4 - 2 + 0) / 1) + 1 = 3x3. We evaluate all 9 receptive fields step-by-step:", bold_prefix="Step-by-Step Receptive Field Calculations: ")
    add_para(doc, "(2×1) + (1×0) + (1×0) + (3×1) = 2 + 0 + 0 + 3 = 5", bold_prefix="• Position (0, 0): ")
    add_para(doc, "(1×1) + (0×0) + (3×0) + (2×1) = 1 + 0 + 0 + 2 = 3", bold_prefix="• Position (0, 1): ")
    add_para(doc, "(0×1) + (3×0) + (2×0) + (1×1) = 0 + 0 + 0 + 1 = 1", bold_prefix="• Position (0, 2): ")
    add_para(doc, "(1×1) + (3×0) + (0×0) + (2×1) = 1 + 0 + 0 + 2 = 3", bold_prefix="• Position (1, 0): ")
    add_para(doc, "(3×1) + (2×0) + (2×0) + (1×1) = 3 + 0 + 0 + 1 = 4", bold_prefix="• Position (1, 1): ")
    add_para(doc, "(2×1) + (1×0) + (1×0) + (0×1) = 2 + 0 + 0 + 0 = 2", bold_prefix="• Position (1, 2): ")
    add_para(doc, "(0×1) + (2×0) + (3×0) + (1×1) = 0 + 0 + 0 + 1 = 1", bold_prefix="• Position (2, 0): ")
    add_para(doc, "(2×1) + (1×0) + (1×0) + (0×1) = 2 + 0 + 0 + 0 = 2", bold_prefix="• Position (2, 1): ")
    add_para(doc, "(1×1) + (0×0) + (0×0) + (2×1) = 1 + 0 + 0 + 2 = 3", bold_prefix="• Position (2, 2): ")

    add_callout(doc, "Resulting Output Feature Map (3x3) = [ [5, 3, 1],  [3, 4, 2],  [1, 2, 3] ]", "Final Output Feature Map after Convolution")

    add_heading(doc, "3. Real-World Applications of CNNs", level=1)
    add_para(doc, "Categorizing whole images into discrete classes (e.g., ImageNet, ResNet, EfficientNet).", bold_prefix="• Image Classification: ")
    add_para(doc, "Simultaneously predicting bounding box coordinates and class labels for multiple entities (e.g., YOLO, Faster R-CNN, SSD).", bold_prefix="• Object Detection and Localization: ")
    add_para(doc, "Assigning semantic class labels to every individual pixel for scene parsing (e.g., Mask R-CNN, U-Net).", bold_prefix="• Semantic and Instance Segmentation: ")
    add_para(doc, "Detecting tumors, lung nodules, retinal pathologies from MRI, CT, and X-ray scans with radiologist-level precision.", bold_prefix="• Medical Diagnostic Imaging: ")
    add_para(doc, "Perception pipelines for lane detection, pedestrian tracking, and traffic sign recognition in real-time camera streams.", bold_prefix="• Autonomous Driving & Robotics: ")
    add_para(doc, "Facial authentication (FaceNet), OCR text extraction, and video action recognition.", bold_prefix="• Biometrics & Video Analytics: ")

def build_q4(doc):
    doc.add_page_break()
    add_question_box(doc, 4, "Explain the basic types of hybrid systems and its necessity.")
    add_heading(doc, "1. The Necessity of Hybrid Systems", level=1)
    add_para(doc, "In soft computing, the primary constituent paradigms—Artificial Neural Networks (ANN), Fuzzy Logic (FL), and Genetic Algorithms (GA)—possess distinct, individual strengths and fundamental weaknesses:")
    add_para(doc, "Excels at pattern recognition, generalization, and learning from raw data, but functions as an opaque 'black box' with no linguistic explanatory power and can get trapped in local minima.", bold_prefix="• Neural Networks: ")
    add_para(doc, "Excels at modeling human linguistic reasoning, vagueness, and expert heuristic knowledge, but lacks automated self-learning, parameter optimization, and adaptability.", bold_prefix="• Fuzzy Logic: ")
    add_para(doc, "Excels at global combinatorial optimization and heuristic search over complex multimodal fitness landscapes, but lacks fine-grained gradient-guided local convergence and direct reasoning mechanisms.", bold_prefix="• Genetic Algorithms: ")
    add_para(doc, "The fundamental necessity of hybrid systems arises from synergy: by synergistically fusing two or more complementary methodologies, the strengths of one paradigm compensate for the limitations of the other, enabling the construction of intelligent systems that are adaptive, interpretable, robust, and capable of global optimization.")

    add_heading(doc, "2. Basic Types of Hybrid Systems", level=1)
    add_para(doc, "Hybrid systems are broadly categorized by the specific constituent technologies combined:")
    
    add_para(doc, "Merges the learning and pattern-matching power of neural networks with the transparent rule-based reasoning of fuzzy logic. The neural network learns, extracts, or tunes membership functions and rule structures from training data. Examples: ANFIS, FALCON, NEFCON.", bold_prefix="1. Neuro-Fuzzy Hybrid Systems (NFHS): ", bullet=True)
    add_para(doc, "Applies genetic algorithms to optimize neural network architecture (number of layers, neuron counts) or synaptic weights. This prevents backpropagation from getting trapped in local minima and automates structural design. Examples: NEAT (NeuroEvolution of Augmenting Topologies).", bold_prefix="2. Neuro-Genetic Hybrid Systems (NGHS): ", bullet=True)
    add_para(doc, "Uses evolutionary algorithms to design and optimize fuzzy rule bases, membership function shapes, and scaling factors. Examples: Pittsburgh, Michigan, and iterative rule learning approaches.", bold_prefix="3. Fuzzy-Genetic Hybrid Systems (FGHS / GFS): ", bullet=True)
    add_para(doc, "Advanced tri-hybrid architectures where genetic algorithms optimize the topology and parameters of a neuro-fuzzy inference system, achieving fully autonomous learning and optimization.", bold_prefix="4. Genetic-Neuro-Fuzzy (Tri-Hybrid Systems): ", bullet=True)

    add_heading(doc, "3. Structural Integration Modes", level=1)
    add_para(doc, "Technologies are connected in a pipeline where the output of one serves as the sequential input to the next (e.g., an ANN extracts features passed to a fuzzy controller).", bold_prefix="• Sequential (Cascade) Hybrid: ")
    add_para(doc, "One technology acts as a secondary supporting or tuning engine for the primary system (e.g., GA optimizes ANN weights offline).", bold_prefix="• Auxiliary Hybrid: ")
    add_para(doc, "The constituent paradigms are fused into a unified internal representation sharing parameters and data structures (e.g., ANFIS where fuzzy parameters exist directly as neural network weights).", bold_prefix="• Embedded (Fully Integrated) Hybrid: ")

def build_q5(doc):
    doc.add_page_break()
    add_question_box(doc, 5, "Compare Artificial Neural Network and Deep Neural Network.")
    add_heading(doc, "Comprehensive Comparison: ANN vs DNN", level=1)
    add_para(doc, "While Deep Neural Networks (DNN) are technically an architectural evolution of Artificial Neural Networks (ANN), their differences in depth, learning mechanics, feature extraction, computational scale, and applications are substantial.")

    headers = ["Comparison Parameter", "Artificial Neural Network (ANN / Shallow)", "Deep Neural Network (DNN)"]
    data = [
        ["Architectural Depth", "Shallow topology; typically consists of 1 or 2 hidden layers between input and output.", "Deep hierarchy; contains multiple hidden layers (ranging from tens to hundreds of layers)."],
        ["Feature Engineering", "Requires manual, domain-specific feature extraction and preprocessing before training.", "Performs automated end-to-end representation learning directly from raw data."],
        ["Hierarchical Abstraction", "Learns simple nonlinear input-to-output mappings; cannot construct deep compositional hierarchies.", "Builds successive layers of abstraction (e.g., pixels → edges → textures → parts → objects)."],
        ["Data Volume Dependency", "Performs effectively on small to moderate datasets; performance quickly plateaus on big data.", "Requires massive datasets to generalize properly; performance continually scales with more data."],
        ["Vanishing / Exploding Gradients", "Rarely encounters severe vanishing gradients due to shallow backpropagation paths.", "Highly susceptible to vanishing/exploding gradients; requires ReLU, BatchNorm, ResNet skips."],
        ["Parameter Complexity", "Thousands to tens of thousands of learnable parameters; low risk of overparameterization.", "Millions to hundreds of billions of parameters; requires strong regularization (Dropout, weight decay)."],
        ["Hardware & Compute", "Can be trained quickly on standard consumer CPUs.", "Requires specialized parallel hardware accelerators (NVIDIA GPUs, Google TPUs) and clusters."],
        ["Training Duration", "Training completes in seconds to minutes.", "Training spans hours, days, or weeks depending on compute infrastructure."],
        ["Canonical Architectures", "Single Layer Perceptron, Multi-Layer Perceptron (MLP), Hopfield Networks, Kohonen SOM.", "CNNs, RNNs, LSTMs, Transformers, ResNets, DenseNets, Diffusion Models, Autoencoders."],
        ["Primary Applications", "Tabular data classification, simple regression, linear pattern recognition, sensor calibration.", "Computer vision, Large Language Models (LLMs), speech recognition, autonomous driving, drug discovery."]
    ]
    add_table_custom(doc, headers, data, [Inches(1.8), Inches(2.5), Inches(2.5)])

def build_q6(doc):
    doc.add_page_break()
    add_question_box(doc, 6, "Explain the working of neuro-genetic hybrid system with neat diagram. Explain its applications and advantages.")
    add_heading(doc, "1. Working Principle of Neuro-Genetic Hybrid Systems", level=1)
    add_para(doc, "A Neuro-Genetic Hybrid System synergistically integrates Genetic Algorithms (GAs) and Artificial Neural Networks (ANNs). Standard gradient descent algorithms (like Backpropagation) are prone to getting trapped in sub-optimal local minima, require differentiable activation functions, and are highly sensitive to initial random weight assignments. Furthermore, backpropagation cannot optimize the topological structure of the network. GAs provide a global, derivative-free, stochastic search mechanism that effectively explores the non-convex weight and architectural space.")

    add_para(doc, "Genetic algorithms can enhance neural networks in three distinct operational modes:", bold_prefix="Operational Modes: ")
    add_para(doc, "The synaptic weights and biases are concatenated into a string of real numbers or binary bits forming a chromosome: C = [w_1, w_2, ..., w_n]. A population of candidate weight vectors is evaluated across training data. Fitness is computed as an inverse of error (e.g., Fitness = 1 / (1 + MSE)). Genetic operators (selection, crossover, mutation) evolve the weights towards global optimality.", bold_prefix="1. Synaptic Weight Optimization: ", bullet=True)
    add_para(doc, "Chromosomes encode network structural hyperparameters (number of hidden layers, number of neurons per layer, connectivity graphs, transfer functions). Popular frameworks like NEAT evolve minimal, optimal topologies alongside weights.", bold_prefix="2. Topology / Architecture Evolution: ", bullet=True)
    add_para(doc, "GA searches for optimal training hyperparameters such as learning rate (η), momentum coefficient (α), and regularization penalties (λ).", bold_prefix="3. Hyperparameter Tuning: ", bullet=True)

    add_heading(doc, "2. Block Diagram and Algorithmic Flow", level=1)
    add_figure(doc, f"{FIG_DIR}/diagram_neuro_genetic.png", "Figure 6.1: Algorithmic Flowchart of Neuro-Genetic Hybrid Optimization.")

    add_para(doc, "Generate an initial population of P chromosomes representing candidate neural networks.", bold_prefix="• Step 1 (Initialization): ")
    add_para(doc, "Instantiate the corresponding neural network for each chromosome and execute a forward pass across training instances to compute error E.", bold_prefix="• Step 2 (Phenotypic Decoding & Evaluation): ")
    add_para(doc, "Assign a fitness value F_i = 1 / (1 + E_i) to each individual.", bold_prefix="• Step 3 (Fitness Calculation): ")
    add_para(doc, "If maximum generations or an acceptable error threshold is achieved, terminate and deploy the optimal neural network.", bold_prefix="• Step 4 (Termination Check): ")
    add_para(doc, "Select fitter parent individuals (via Roulette Wheel or Tournament selection), apply crossover (single-point, two-point, or uniform) to exchange sub-structures, and apply mutation (Gaussian perturbation) to maintain diversity. The offspring form the new generation.", bold_prefix="• Step 5 (Reproduction & Variation): ")

    add_heading(doc, "3. Applications and Advantages", level=1)
    add_para(doc, "Robotic motion planning, inverse kinematics, and bipedal locomotion where exact analytical gradients are intractable.", bold_prefix="• Autonomous Robotics & Control: ")
    add_para(doc, "Non-stationary algorithmic trading, portfolio management, and stock index forecasting.", bold_prefix="• Financial Market Forecasting: ")
    add_para(doc, "Deep reinforcement learning agents playing complex strategy games (Atari, StarCraft, Mario) without gradient backpropagation.", bold_prefix="• Game AI & Neuroevolution: ")
    add_para(doc, "Global optimization bypasses local minima traps; derivative-free learning accommodates non-differentiable objectives; automated discovery of compact architectures reduces overfitting; naturally suited for parallel processing.", bold_prefix="• Key Advantages: ")

def build_q7(doc):
    doc.add_page_break()
    add_question_box(doc, 7, "Explain various methods of pooling in CNN with suitable example.")
    add_heading(doc, "1. Purpose and Mechanics of Pooling in CNN", level=1)
    add_para(doc, "Pooling (also called subsampling or downsampling) is a non-learnable spatial reduction operation inserted periodically between successive convolutional layers in a CNN. It slides a 2D pooling window (typically 2x2 with stride 2) across input feature maps to aggregate local activations into single representative values.")
    
    add_para(doc, "Pooling provides three vital benefits:", bold_prefix="Primary Objectives: ")
    add_para(doc, "Reduces feature map height and width by 50% (at stride 2), cutting spatial dimensions and computational FLOPs by 75% for subsequent layers.", bold_prefix="1. Spatial Dimension Reduction: ", bullet=True)
    add_para(doc, "Small translations or distortions of features in the input image do not alter the pooled outputs, imparting robustness.", bold_prefix="2. Translation Invariance: ", bullet=True)
    add_para(doc, "By shrinking spatial extent, subsequent convolutional filters cover a larger effective region of the original raw input image.", bold_prefix="3. Receptive Field Expansion: ", bullet=True)

    add_heading(doc, "2. Various Methods of Pooling", level=1)
    add_para(doc, "Selects the maximum value within the pooling window:  y_{i, j} = max_{(m, n) ∈ R_{i, j}} x_{m, n}. It captures the most prominent, sharp features (edges, textures, prominent activations) while discarding background noise. It is the dominant pooling technique in modern computer vision.", bold_prefix="1. Max Pooling: ", bullet=True)
    add_para(doc, "Computes the arithmetic mean of all activations within the pooling window:  y_{i, j} = (1 / |R_{i, j}|) Σ_{(m, n) ∈ R_{i, j}} x_{m, n}. It smooths features and retains ambient background context, though it can dilute sharp feature activations.", bold_prefix="2. Average Pooling: ", bullet=True)
    add_para(doc, "Takes an entire H×W feature map channel and computes the average across all spatial locations, outputting a single 1×1 scalar per channel. Pioneered by Lin et al. (Network in Network) and popularized by ResNet, GAP replaces heavy fully connected layers before classification, slashing millions of parameters and preventing overfitting.", bold_prefix="3. Global Average Pooling (GAP): ", bullet=True)
    add_para(doc, "Extracts the single maximum activation across the entire H×W channel. Highly useful in weakly supervised object localization.", bold_prefix="4. Global Max Pooling (GMP): ", bullet=True)
    add_para(doc, "Computes the square root of the sum of squared activations within the window:  y_{i, j} = √[ Σ x_{m, n}² ]. Generalizes average pooling with stronger emphasis on higher activations.", bold_prefix="5. L2 (Norm) Pooling: ", bullet=True)
    add_para(doc, "Instead of a deterministic max or mean, it samples activations from a multinomial distribution where probabilities are proportional to feature magnitudes: p_i = a_i / Σ a_k. Acts as an effective regularizer to prevent overfitting.", bold_prefix="6. Stochastic Pooling: ", bullet=True)

    add_heading(doc, "3. Comparative Worked Example", level=1)
    add_para(doc, "Consider a 4x4 input matrix with a 2x2 pooling window and stride 2:")
    add_callout(doc, "Input Matrix = [ [12, 20, 30, 0],  [8, 12, 2, 0],  [34, 70, 37, 4],  [112, 100, 25, 12] ]", "Illustrative 4x4 Feature Map")
    
    add_para(doc, "Top-Left [12, 20; 8, 12] → max = 20; Top-Right [30, 0; 2, 0] → max = 30;\nBottom-Left [34, 70; 112, 100] → max = 112; Bottom-Right [37, 4; 25, 12] → max = 37.\nOutput = [ [20, 30],  [112, 37] ]", bold_prefix="• Max Pooling Result (2x2): ")
    add_para(doc, "Top-Left mean = (12+20+8+12)/4 = 52/4 = 13.0;\nTop-Right mean = (30+0+2+0)/4 = 32/4 = 8.0;\nBottom-Left mean = (34+70+112+100)/4 = 316/4 = 79.0;\nBottom-Right mean = (37+4+25+12)/4 = 78/4 = 19.5.\nOutput = [ [13.0, 8.0],  [79.0, 19.5] ]", bold_prefix="• Average Pooling Result (2x2): ")

def build_q8(doc):
    doc.add_page_break()
    add_question_box(doc, 8, "List different types of Autoencoder. Explain the working of Under-complete Autoencoder.")
    add_heading(doc, "1. Comprehensive List of Autoencoder Types", level=1)
    add_para(doc, "1. Undercomplete Autoencoder (bottleneck dimension strictly less than input dimension)\n2. Overcomplete Autoencoder (latent dimension equal to or exceeding input dimension)\n3. Sparse Autoencoder (SAE - penalized by activation sparsity constraints such as KL divergence)\n4. Denoising Autoencoder (DAE - trained to reconstruct clean data from noise-corrupted inputs)\n5. Contractive Autoencoder (CAE - regularized with the Frobenius norm of the encoder Jacobian)\n6. Variational Autoencoder (VAE - probabilistic generative model optimizing the ELBO)\n7. Convolutional Autoencoder (CAE - utilizes 2D convolutional and deconvolutional operations)\n8. Recurrent / Sequence-to-Sequence Autoencoder (LSTM/GRU-based autoencoder for temporal sequences)")

    add_heading(doc, "2. Detailed Working of Under-complete Autoencoder", level=1)
    add_para(doc, "An Under-complete Autoencoder is the most fundamental autoencoder architecture. Its defining architectural trait is that the latent code layer z has strictly lower dimensionality than the input space x (i.e., d < D, where x ∈ ℝᴰ and z ∈ ℝᵈ).")

    add_para(doc, "The primary mechanism and operational principles include:", bold_prefix="Operational Mechanics: ")
    add_para(doc, "If an autoencoder were given unlimited hidden capacity, it could trivially learn the identity function x̂ = x by copying inputs to outputs without discovering meaningful representations. By constraining the bottleneck dimension d < D, an informational bottleneck is created. The network cannot copy data; it is forced to discover and encode only the most salient, non-redundant latent factors of variation.", bold_prefix="1. The Bottleneck Constraint: ", bullet=True)
    add_para(doc, "Encoder maps input x to latent code: z = σ(W_e x + b_e), with W_e ∈ ℝᵈˣᴰ. Decoder maps code z back to reconstructed space: x̂ = σ'(W_d z + b_d), with W_d ∈ ℝᴰˣᵈ. Frequently, tied weights are used (W_d = W_eᵀ) to halve parameter count and act as a regularizer.", bold_prefix="2. Mathematical Formulation: ", bullet=True)
    add_para(doc, "The network is trained end-to-end via gradient backpropagation to minimize reconstruction loss: L(x, x̂) = (1/2) Σ_{j=1}^D (x_j - x̂_j)².", bold_prefix="3. Optimization Objective: ", bullet=True)
    
    add_callout(doc, "Relationship to PCA: If both encoder and decoder use purely LINEAR activation functions, an undercomplete autoencoder learns the exact same subspace as Principal Component Analysis (PCA). With NONLINEAR activations (e.g., ReLU, Sigmoid), it generalizes PCA to learn complex, curved nonlinear manifolds.", "PCA Equivalence and Nonlinear Generalization")

    add_para(doc, "Undercomplete autoencoders are widely employed for lossy data compression, feature extraction for downstream classifiers, noise reduction, and low-dimensional data visualization.", bold_prefix="• Applications: ")
    add_para(doc, "If the network depth and capacity are excessively large without regularization, it may still overfit or memorize specific training instances rather than discovering smooth semantic manifolds.", bold_prefix="• Limitations: ")

def build_q9(doc):
    doc.add_page_break()
    add_question_box(doc, 9, "What are co-operative neuro-fuzzy hybrid systems? Explain its types.")
    add_heading(doc, "1. Concept of Co-operative Neuro-Fuzzy Systems", level=1)
    add_para(doc, "In a Co-operative Neuro-Fuzzy System, Artificial Neural Networks (ANN) and Fuzzy Logic Systems (FLS) function as distinct, autonomous modular entities cooperating in separate phases to achieve a common task. Unlike fully integrated/fused hybrid systems (such as ANFIS, where fuzzy reasoning is permanently embedded as synaptic weights inside a single network), a co-operative system maintains an architectural separation between the learning engine and the execution engine.")
    
    add_para(doc, "Typically, the neural network is utilized offline to learn, extract, or fine-tune fuzzy parameters (such as membership function shapes or rule antecedents/consequents) from numerical training data. Once learning converges, the learned parameters are transferred to the Fuzzy Logic Controller, the neural network is discarded, and the fuzzy system runs independently during runtime execution.")

    add_heading(doc, "2. Types of Co-operative Neuro-Fuzzy Systems", level=1)
    add_para(doc, "Co-operative architectures are classified according to the specific role fulfilled by the neural network:")

    add_para(doc, "A multi-layer neural network is first trained on empirical input-output data. After convergence, the internal weights, hidden layer activation clusters, and activation paths are mathematically analyzed and pruned to extract explicit linguistic IF-THEN fuzzy rules (e.g., 'IF Speed is High AND Distance is Short THEN Brake is Maximum'). This eliminates reliance on subjective human domain experts.", bold_prefix="1. Neural Network for Fuzzy Rule Extraction: ", bullet=True)
    add_para(doc, "Fuzzy rules are established a priori by human experts, but the exact parameterization of membership functions (e.g., center, spread, slope of Gaussian/triangular sets) is imprecise. A neural network uses backpropagation over sample data to iteratively adjust and calibrate the membership function parameters to minimize system error.", bold_prefix="2. Neural Network for Membership Function Tuning: ", bullet=True)
    add_para(doc, "The fuzzy antecedent conditions (IF parts) and membership functions remain fixed. The neural network learns the optimal consequent parameters (THEN parts)—either singletons, linear coefficients, or fuzzy output sets—by matching target outputs.", bold_prefix="3. Neural Network for Fuzzy Consequent Learning: ", bullet=True)
    add_para(doc, "The neural network and fuzzy system operate in a multi-stage execution pipeline. The neural network acts as a front-end feature extractor, processing noisy, high-dimensional raw sensory signals into filtered, high-level features. These features are then supplied to the fuzzy controller for transparent, explainable decision-making.", bold_prefix="4. Cascaded / Sequential Co-operative Hybrid: ", bullet=True)

    headers = ["Co-operative Type", "Primary Role of ANN", "Primary Role of Fuzzy System", "Key Benefit"]
    data = [
        ["Rule Extraction", "Discovers rule structures from raw data.", "Executes linguistic reasoning.", "Automates rule generation without expert."],
        ["Parameter Tuning", "Optimizes membership function parameters.", "Executes fuzzy inference with tuned sets.", "Maximizes precision and minimizes error."],
        ["Consequent Learning", "Learns optimal output weights/singletons.", "Supplies rule firing strengths.", "Accelerates convergence on complex targets."],
        ["Cascaded Architecture", "Preprocesses raw high-dimensional data.", "Performs transparent high-level control.", "High noise immunity and interpretability."]
    ]
    add_table_custom(doc, headers, data, [Inches(1.6), Inches(2.2), Inches(2.2), Inches(1.8)])

def build_q10(doc):
    doc.add_page_break()
    add_question_box(doc, 10, "Draw the block diagram of Genetic Fuzzy Rule Based System and explain in detail.")
    add_heading(doc, "1. Architecture of Genetic Fuzzy Rule-Based Systems (GFRBS)", level=1)
    add_para(doc, "A Genetic Fuzzy Rule-Based System (GFRBS) is an evolutionary hybrid system that utilizes Genetic Algorithms (GAs) to automate the design, optimization, and structural learning of a Fuzzy Rule-Based System (FRBS). Creating an effective FRBS manually is difficult due to the subjective nature of defining membership functions and the combinatorial complexity of formulating complete fuzzy rule bases. GFRBS solves this by treating fuzzy system design as an evolutionary search problem over a parameter space.")

    add_figure(doc, f"{FIG_DIR}/diagram_gfrbs.png", "Figure 10.1: Structural Block Diagram of a Genetic Fuzzy Rule-Based System (GFRBS).")

    add_para(doc, "A GFRBS comprises the following core components:", bold_prefix="Component Descriptions: ")
    add_para(doc, "Stores the mathematical parameters defining the fuzzy membership functions (centers, widths, shapes), universe of discourse, and scaling factors.", bold_prefix="1. Data Base (DB): ", bullet=True)
    add_para(doc, "Contains the collection of linguistic IF-THEN fuzzy rules that govern system behavior. Together, DB + RB constitute the Knowledge Base (KB).", bold_prefix="2. Rule Base (RB): ", bullet=True)
    add_para(doc, "Executes fuzzy reasoning (fuzzification, inference via T-norm/T-conorm, and defuzzification to produce crisp outputs).", bold_prefix="3. Fuzzy Inference Engine: ", bullet=True)
    add_para(doc, "Manages a population of candidate solutions (chromosomes). It decodes chromosomes into candidate fuzzy components, evaluates their performance via a fitness function across training data, and applies selection, crossover, and mutation to generate improved generations.", bold_prefix="4. Genetic Learning Module: ", bullet=True)

    add_heading(doc, "2. Dominant Evolutionary Approaches: Pittsburgh vs. Michigan", level=1)
    add_para(doc, "The two principal paradigms for encoding fuzzy rules in genetic chromosomes are:")

    add_para(doc, "Each chromosome represents an ENTIRE fuzzy rule base (a complete set of candidate rules). The genetic population consists of multiple complete rule bases competing against one another. Advantages: Directly models inter-rule interactions and co-adaptation; can optimize the total number of rules automatically. Disadvantages: Chromosomes are very long, leading to large search spaces and substantial computational cost.", bold_prefix="1. The Pittsburgh Approach (Rule-Set Level): ", bullet=True)
    add_para(doc, "Each chromosome represents a SINGLE individual fuzzy rule. The ENTIRE population collectively forms the complete fuzzy rule base. Rules cooperate to solve the task. Advantages: Chromosomes are compact and short, resulting in fast evaluations. Disadvantages: Credit assignment is complex (determining how much an individual rule contributed to overall system success); risk of internal competition rather than cooperation among rules.", bold_prefix="2. The Michigan Approach (Individual Rule Level): ", bullet=True)
    add_para(doc, "A hybrid approach where chromosomes encode single rules, but rules are learned sequentially one at a time. Once an optimal rule is found, the training instances it covers are masked or penalized, forcing subsequent iterations to learn rules for remaining input regions.", bold_prefix="3. Iterative Rule Learning (IRL): ", bullet=True)

    headers = ["Feature", "Pittsburgh Approach", "Michigan Approach", "Iterative Rule Learning (IRL)"]
    data = [
        ["Chromosome Representation", "Entire complete Rule Base (RB)", "A single individual fuzzy rule", "A single individual fuzzy rule"],
        ["Population Role", "A collection of competing rule bases", "Collectively forms one single rule base", "Explores rules for uncovered data"],
        ["Chromosome Length", "Variable and very long", "Fixed and short", "Fixed and short"],
        ["Rule Interaction", "Explicitly evaluated across all rules", "Implicit / credit assignment challenge", "Handled iteratively via data masking"],
        ["Computational Cost", "High (evaluates entire rule bases)", "Moderate / Low", "Moderate"]
    ]
    add_table_custom(doc, headers, data, [Inches(1.5), Inches(2.1), Inches(2.1), Inches(1.8)])

def build_q11(doc):
    doc.add_page_break()
    add_question_box(doc, 11, "Discuss briefly Recurrent Neural Networks and list the various tasks they can perform. How does it differ from Recursive Neural Networks?")
    add_heading(doc, "1. Recurrent Neural Networks (RNN) and Mathematical Foundations", level=1)
    add_para(doc, "A Recurrent Neural Network (RNN) is a class of artificial neural networks designed specifically for processing sequential, time-series, or temporal data. Unlike standard feedforward networks that assume all inputs are independent, RNNs contain internal feedback loops. This recurrence creates an internal memory or 'hidden state' h_t that retains contextual information from previous time steps to inform future predictions.")

    add_callout(doc, "Hidden State Update:  h_t = tanh( W_{hh} h_{t-1} + W_{xh} x_t + b_h )\nOutput Generation:   y_t = softmax( W_{hy} h_t + b_y )", "Mathematical Formulation of Standard Elman RNN")
    
    add_para(doc, "RNNs are trained using Backpropagation Through Time (BPTT), which unrolls the recurrence graph across discrete time steps. To combat the severe vanishing/exploding gradient problems encountered across long sequences, gated variants such as Long Short-Term Memory (LSTM) and Gated Recurrent Units (GRU) are standardly employed.")

    add_heading(doc, "2. Operational Tasks Performed by RNNs", level=1)
    add_para(doc, "RNN computational tasks are classified by input/output sequence structures:")
    add_para(doc, "Standard feedforward mode (e.g., static image classification).", bold_prefix="• One-to-One: ")
    add_para(doc, "A single static input produces a sequence of outputs (e.g., Image Captioning: image → sequence of descriptive words).", bold_prefix="• One-to-Many: ")
    add_para(doc, "A sequence of inputs produces a single output (e.g., Sentiment Analysis: sentence of words → sentiment score; Video activity classification).", bold_prefix="• Many-to-One: ")
    add_para(doc, "Input and output sequences of equal length processed in lock-step (e.g., Named Entity Recognition, POS tagging, video frame labeling).", bold_prefix="• Many-to-Many (Synchronized): ")
    add_para(doc, "Sequence-to-Sequence (Seq2Seq) encoder-decoder models where input and output sequence lengths vary (e.g., Machine Translation, Speech-to-Text, Conversational Chatbots).", bold_prefix="• Many-to-Many (Asynchronous): ")

    add_heading(doc, "3. Differences: Recurrent vs. Recursive Neural Networks", level=1)
    add_figure(doc, f"{FIG_DIR}/diagram_rnn_vs_recursive.png", "Figure 11.1: Structural Comparison of Recurrent Neural Networks (Linear Temporal Chain) and Recursive Neural Networks (Hierarchical Tree Structure).")

    headers = ["Aspect", "Recurrent Neural Network (RNN)", "Recursive Neural Network (Tree-RNN)"]
    data = [
        ["Network Topology", "Linear 1D chain unrolled strictly over sequential time steps.", "Hierarchical Directed Acyclic Graph (DAG) or tree structure."],
        ["Input Structure", "1D temporal sequences, time series, audio waveforms, text streams.", "Hierarchical structures, grammatical parse trees, molecular graphs."],
        ["Recurrence Mechanism", "Recurrence propagates linearly: h_t = f(h_{t-1}, x_t).", "Recurrence combines child nodes into parent: h_{parent} = f(h_{child1}, h_{child2})."],
        ["Computational Ordering", "Temporal / sequential ordering (past to future).", "Spatial / syntactic compositional hierarchy (leaves to root)."],
        ["Time vs Structure", "Explicitly models temporal passage of time and sequence position.", "Explicitly models structural compositionality and semantic hierarchy."],
        ["Primary Applications", "Speech recognition, language modeling, time-series forecasting.", "Natural language syntactic parsing, sentence sentiment trees, chemical property prediction."]
    ]
    add_table_custom(doc, headers, data, [Inches(1.4), Inches(2.8), Inches(2.8)])

def build_q12(doc):
    doc.add_page_break()
    add_question_box(doc, 12, "Discuss the need for Auto-encoders in Deep Neural Architectures. Explain the various Hyper-parameters that we need to set before training an auto-encoder. Why are auto-encoders preferred over PCA?")
    add_heading(doc, "1. Need for Autoencoders in Deep Neural Architectures", level=1)
    add_para(doc, "Autoencoders serve critical functions in modern deep learning pipelines:", bold_prefix="Architectural Roles: ")
    add_para(doc, "In the early development of deep networks, end-to-end backpropagation failed due to vanishing gradients. Stacked Autoencoders enabled 'Greedy Layer-Wise Pre-training' (Hinton & Bengio), initializing weights near good local basins of attraction prior to supervised fine-tuning.", bold_prefix="1. Unsupervised Pre-training & Initialization: ", bullet=True)
    add_para(doc, "High-dimensional real-world data concentrates along low-dimensional curved manifolds. Autoencoders discover these nonlinear manifolds, stripping away redundant noise.", bold_prefix="2. Manifold Learning & Dimensionality Reduction: ", bullet=True)
    add_para(doc, "When trained solely on normal baseline patterns, an autoencoder yields low reconstruction error on normal data but high error on anomalies. This makes it ideal for fraud detection, industrial defect detection, and cyber-intrusion detection.", bold_prefix="3. Anomaly and Novelty Detection: ", bullet=True)
    add_para(doc, "Variational Autoencoders (VAEs) structure the latent space into smooth continuous distributions, enabling generative sampling of new realistic data (images, molecules, speech).", bold_prefix="4. Generative Modeling & Data Synthesis: ", bullet=True)

    add_heading(doc, "2. Hyperparameters to Set Before Training an Autoencoder", level=1)
    add_para(doc, "The number of neurons in the central bottleneck layer. Setting d < D controls the compression ratio and information capacity.", bold_prefix="1. Code (Bottleneck) Size: ", bullet=True)
    add_para(doc, "The total count of hidden layers in the encoder and decoder. Deeper autoencoders can model exponentially more complex hierarchical manifolds.", bold_prefix="2. Network Depth: ", bullet=True)
    add_para(doc, "The distribution of neuron counts per layer (e.g., symmetric pyramid: 784 → 256 → 64 → 32 → 64 → 256 → 784).", bold_prefix="3. Layer Widths (Nodes per Layer): ", bullet=True)
    add_para(doc, "Selected based on input data type: Mean Squared Error (MSE) for unbounded continuous variables; Binary Cross-Entropy for normalized [0, 1] pixels.", bold_prefix="4. Reconstruction Loss Function: ", bullet=True)
    add_para(doc, "Hidden layer activations (ReLU, LeakyReLU, ELU) and output activations (Sigmoid for [0, 1] bounded outputs; Linear for unbounded outputs).", bold_prefix="5. Activation Functions: ", bullet=True)
    add_para(doc, "Sparsity target ρ̂ and penalty weight β (Sparse AE); Noise standard deviation σ (Denoising AE); Frobenius penalty weight λ (Contractive AE); KL loss weight β (β-VAE).", bold_prefix="6. Regularization Hyperparameters: ", bullet=True)
    add_para(doc, "Optimizer (Adam, RMSprop, SGD), learning rate schedule, batch size, and epoch count.", bold_prefix="7. Optimization Parameters: ", bullet=True)

    add_heading(doc, "3. Why Autoencoders are Preferred Over PCA", level=1)
    headers = ["Criterion", "Principal Component Analysis (PCA)", "Autoencoders (Neural Network)"]
    data = [
        ["Mapping Nature", "Strictly LINEAR transformation (orthogonal hyperplane projection).", "NONLINEAR transformation (via nonlinear activation functions), learning curved manifolds."],
        ["Hierarchical Depth", "Single-stage flat projection; no multi-level feature abstractions.", "Deep hierarchical architectures learn successive levels of feature abstraction."],
        ["Spatial / Temporal Structure", "Flattens data into 1D vectors; ignores 2D grid or temporal relationships.", "Can use Convolutional (2D/3D) or Recurrent (LSTM) layers, preserving spatial/temporal structure."],
        ["Generative Modeling", "Cannot effectively sample novel synthetic instances from complex distributions.", "Variational Autoencoders (VAEs) provide smooth latent distributions for data generation."],
        ["Loss Function Flexibility", "Strictly minimizes Mean Squared Error (L2 reconstruction / variance).", "Can optimize custom task losses (Perceptual loss, Cross-Entropy, adversarial losses)."],
        ["Computational Scaling", "Requires computing SVD/eigen-decomposition of covariance matrix (expensive on big data).", "Trained with mini-batch Stochastic Gradient Descent; scales gracefully to millions of samples."]
    ]
    add_table_custom(doc, headers, data, [Inches(1.6), Inches(2.7), Inches(2.7)])

def build_q13(doc):
    doc.add_page_break()
    add_question_box(doc, 13, "Why is pooling needed in a Convolutional Neural Network? Discuss the Max-pooling and Average pooling techniques. Perform Max and Average pooling on the given data with filter size 2 and stride 2.")
    add_heading(doc, "1. Need for Pooling in Convolutional Neural Networks", level=1)
    add_para(doc, "Pooling is indispensable in CNN architectures for the following fundamental reasons:", bold_prefix="Key Rationale: ")
    add_para(doc, "Reduces the spatial dimensions (height and width) of feature maps progressively, drastically cutting down memory consumption and arithmetic FLOPs required in subsequent layers.", bold_prefix="• Dimensionality Reduction: ")
    add_para(doc, "Fewer parameters in subsequent layers lowers model capacity, acting as an effective structural regularizer against overfitting.", bold_prefix="• Overfitting Prevention: ")
    add_para(doc, "Ensures that small shifts, rotations, or distortions of an object in the input image do not alter the pooled feature representations.", bold_prefix="• Translation Invariance: ")
    add_para(doc, "Subsampling expands the effective receptive field of neurons in deeper layers, enabling them to capture larger contextual features of the input scene.", bold_prefix="• Receptive Field Enlargement: ")

    add_heading(doc, "2. Max-Pooling vs. Average Pooling", level=1)
    add_para(doc, "Selects the maximum value within each pooling window:  y = max(R). It retains the most prominent, high-frequency activations (such as edges, corners, and strong textural features) while suppressing background noise. It is by far the most prevalent pooling technique in modern classification and detection networks.", bold_prefix="• Max-Pooling: ")
    add_para(doc, "Computes the arithmetic average of all values within the window:  y = (1 / |R|) Σ x. It smooths the feature map and preserves general background presence, but can dilute sharp signals by averaging high activations with low background values.", bold_prefix="• Average Pooling: ")

    add_heading(doc, "3. Step-by-Step Pooling Execution on Given Data", level=1)
    add_para(doc, "We are given the following 4x4 input feature map from the assignment specification:")
    
    add_callout(doc, "Input Matrix (4x4) =\n[ [ 5,  6,  8,  5 ],\n  [ 4,  2,  9,  4 ],\n  [ 7,  6,  7,  3 ],\n  [ 9,  2,  1,  3 ] ]", "Given Assignment 4x4 Input Matrix")

    add_para(doc, "Filter size f = 2, Stride s = 2, Padding p = 0.", bold_prefix="Operation Parameters: ")
    add_para(doc, "W_out = floor((W_in - f + 2p) / s) + 1 = floor((4 - 2 + 0) / 2) + 1 = (2 / 2) + 1 = 2.\nH_out = floor((H_in - f + 2p) / s) + 1 = floor((4 - 2 + 0) / 2) + 1 = (2 / 2) + 1 = 2.\nThus, the pooled output is a 2x2 matrix.", bold_prefix="Output Dimension Calculation: ")

    add_figure(doc, f"{FIG_DIR}/diagram_pooling_q13.png", "Figure 13.1: Visual partitioning of the 4x4 input matrix into 4 non-overlapping quadrants, and resulting 2x2 Max-Pooled and Average-Pooled matrices.", width=Inches(5.6))

    add_para(doc, "With filter size 2x2 and stride s = 2, the 4x4 matrix partitions into 4 non-overlapping 2x2 quadrants:", bold_prefix="Quadrant Calculations: ")
    
    add_para(doc, "Sub-matrix: [ [5, 6], [4, 2] ]\n• Max-Pooling: max(5, 6, 4, 2) = 6\n• Average-Pooling: (5 + 6 + 4 + 2) / 4 = 17 / 4 = 4.25", bold_prefix="1. Quadrant 1 (Top-Left, Rows 0-1, Cols 0-1): ", bullet=True)
    
    add_para(doc, "Sub-matrix: [ [8, 5], [9, 4] ]\n• Max-Pooling: max(8, 5, 9, 4) = 9\n• Average-Pooling: (8 + 5 + 9 + 4) / 4 = 26 / 4 = 6.50", bold_prefix="2. Quadrant 2 (Top-Right, Rows 0-1, Cols 2-3): ", bullet=True)
    
    add_para(doc, "Sub-matrix: [ [7, 6], [9, 2] ]\n• Max-Pooling: max(7, 6, 9, 2) = 9\n• Average-Pooling: (7 + 6 + 9 + 2) / 4 = 24 / 4 = 6.00", bold_prefix="3. Quadrant 3 (Bottom-Left, Rows 2-3, Cols 0-1): ", bullet=True)
    
    add_para(doc, "Sub-matrix: [ [7, 3], [1, 3] ]\n• Max-Pooling: max(7, 3, 1, 3) = 7\n• Average-Pooling: (7 + 3 + 1 + 3) / 4 = 14 / 4 = 3.50", bold_prefix="4. Quadrant 4 (Bottom-Right, Rows 2-3, Cols 2-3): ", bullet=True)

    add_callout(doc, "Max-Pooling Output (2x2) =\n[ [ 6,  9 ],\n  [ 9,  7 ] ]\n\nAverage-Pooling Output (2x2) =\n[ [ 4.25,  6.50 ],\n  [ 6.00,  3.50 ] ]", "Final Solved Output Matrices for Question 13")

# ----------------- MAIN GENERATOR -----------------

def main():
    print("Starting Assignment 2 Document Generation...")
    doc = docx.Document()
    set_footer_and_header(doc)

    print("Adding Header Card and Student Details...")
    add_header_card(doc)

    print("Generating Question 1...")
    build_q1(doc)

    print("Generating Question 2...")
    build_q2(doc)

    print("Generating Question 3...")
    build_q3(doc)

    print("Generating Question 4...")
    build_q4(doc)

    print("Generating Question 5...")
    build_q5(doc)

    print("Generating Question 6...")
    build_q6(doc)

    print("Generating Question 7...")
    build_q7(doc)

    print("Generating Question 8...")
    build_q8(doc)

    print("Generating Question 9...")
    build_q9(doc)

    print("Generating Question 10...")
    build_q10(doc)

    print("Generating Question 11...")
    build_q11(doc)

    print("Generating Question 12...")
    build_q12(doc)

    print("Generating Question 13...")
    build_q13(doc)

    print(f"Saving DOCX to {DOCX_OUT_LAB}...")
    doc.save(DOCX_OUT_LAB)

    print(f"Copying DOCX to {DOCX_OUT_DOWN}...")
    shutil.copyfile(DOCX_OUT_LAB, DOCX_OUT_DOWN)

    print("Converting DOCX to PDF using LibreOffice...")
    cmd = [
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", "/Users/sanjaywaradkar/SC_Lab",
        DOCX_OUT_LAB
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("LibreOffice stdout:", res.stdout)
    if res.stderr:
        print("LibreOffice stderr:", res.stderr)

    if os.path.exists(PDF_OUT_LAB):
        print(f"Copying PDF to {PDF_OUT_DOWN}...")
        shutil.copyfile(PDF_OUT_LAB, PDF_OUT_DOWN)
        print("PDF successfully generated and placed in both locations!")
    else:
        print("Error: PDF generation failed.")

if __name__ == '__main__':
    main()
