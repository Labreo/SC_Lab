import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

os.makedirs('/Users/sanjaywaradkar/SC_Lab/figures', exist_ok=True)
FIG_DIR = '/Users/sanjaywaradkar/SC_Lab/figures'

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# 1. Autoencoder Architecture
def make_autoencoder_diagram():
    fig, ax = plt.subplots(figsize=(8, 3.2), dpi=200)
    ax.axis('off')

    # Draw layers
    layers = [
        ("Input\n$x \in \mathbb{R}^D$", 5, 1.0, '#3182CE'),
        ("Hidden 1\n(Encoder)", 4, 2.5, '#4299E1'),
        ("Latent Code\n$z \in \mathbb{R}^d$ (Bottleneck)", 2, 4.0, '#E53E3E'),
        ("Hidden 2\n(Decoder)", 4, 5.5, '#4299E1'),
        ("Reconstruction\n$\hat{x} \in \mathbb{R}^D$", 5, 7.0, '#3182CE')
    ]

    for name, n_nodes, x_pos, col in layers:
        y_positions = np.linspace(0.5, 3.5, n_nodes)
        for y in y_positions:
            circle = plt.Circle((x_pos, y), 0.18, color=col, ec='#1A202C', lw=1.5, zorder=3)
            ax.add_patch(circle)
        ax.text(x_pos, -0.1, name, ha='center', va='top', fontsize=9, fontweight='bold', color='#1A202C')

    # Draw connections
    for i in range(len(layers)-1):
        x1 = layers[i][2]
        x2 = layers[i+1][2]
        y1_arr = np.linspace(0.5, 3.5, layers[i][1])
        y2_arr = np.linspace(0.5, 3.5, layers[i+1][1])
        for y1 in y1_arr:
            for y2 in y2_arr:
                ax.plot([x1+0.18, x2-0.18], [y1, y2], color='#CBD5E0', lw=0.6, zorder=1)

    # Brackets/Labels
    ax.annotate('', xy=(3.8, 4.0), xytext=(1.2, 4.0),
                arrowprops=dict(arrowstyle="->", lw=2, color='#2B6CB0'))
    ax.text(2.5, 4.15, "Encoder $f_\\theta(x) = \\sigma(W_e x + b_e)$", ha='center', fontsize=9, fontweight='bold', color='#2B6CB0')

    ax.annotate('', xy=(6.8, 4.0), xytext=(4.2, 4.0),
                arrowprops=dict(arrowstyle="->", lw=2, color='#2B6CB0'))
    ax.text(5.5, 4.15, "Decoder $g_{\\theta'}(z) = \\sigma'(W_d z + b_d)$", ha='center', fontsize=9, fontweight='bold', color='#2B6CB0')

    # Loss comparison
    ax.text(4.0, -0.6, "Reconstruction Loss: $\mathcal{L}(x, \hat{x}) = \\frac{1}{2} ||x - \hat{x}||^2$",
            ha='center', fontsize=10, fontweight='bold', color='#C53030',
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFF5F5", ec="#FEB2B2", lw=1.2))

    ax.set_xlim(0, 8)
    ax.set_ylim(-0.9, 4.6)
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/diagram_autoencoder.png', bbox_inches='tight')
    plt.close()

# 2. Neuro-Fuzzy (ANFIS) Architecture
def make_anfis_diagram():
    fig, ax = plt.subplots(figsize=(8.5, 4.0), dpi=200)
    ax.axis('off')

    layers = [
        ("Layer 1\nFuzzification", 1.2),
        ("Layer 2\nRule Firing (T-Norm)", 3.0),
        ("Layer 3\nNormalization", 4.8),
        ("Layer 4\nConsequent (TSK)", 6.6),
        ("Layer 5\nOverall Output", 8.4)
    ]

    for title, x in layers:
        ax.text(x, 3.8, title, ha='center', fontsize=8.5, fontweight='bold', color='#2C5282',
                bbox=dict(boxstyle="round,pad=0.3", fc="#EBF8FF", ec="#90CDF4", lw=1))

    # Inputs x and y
    ax.text(0.1, 2.7, "$x$", fontsize=12, fontweight='bold', va='center', ha='center',
            bbox=dict(boxstyle="circle,pad=0.3", fc="#EDF2F7", ec="#4A5568"))
    ax.text(0.1, 1.1, "$y$", fontsize=12, fontweight='bold', va='center', ha='center',
            bbox=dict(boxstyle="circle,pad=0.3", fc="#EDF2F7", ec="#4A5568"))

    # Layer 1 nodes: A1, A2, B1, B2
    l1_nodes = [("$A_1$", 1.2, 3.1), ("$A_2$", 1.2, 2.3), ("$B_1$", 1.2, 1.5), ("$B_2$", 1.2, 0.7)]
    for lbl, x, y in l1_nodes:
        box = patches.FancyBboxPatch((x-0.35, y-0.25), 0.7, 0.5, boxstyle="square,pad=0", fc="#BEE3F8", ec="#2B6CB0", lw=1.2)
        ax.add_patch(box)
        ax.text(x, y, lbl, ha='center', va='center', fontsize=9, fontweight='bold')

    ax.annotate('', xy=(0.85, 3.1), xytext=(0.3, 2.7), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))
    ax.annotate('', xy=(0.85, 2.3), xytext=(0.3, 2.7), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))
    ax.annotate('', xy=(0.85, 1.5), xytext=(0.3, 1.1), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))
    ax.annotate('', xy=(0.85, 0.7), xytext=(0.3, 1.1), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))

    # Layer 2: Rule nodes (Pi)
    l2_nodes = [("$\Pi$\n$w_1$", 3.0, 2.7), ("$\Pi$\n$w_2$", 3.0, 1.1)]
    for lbl, x, y in l2_nodes:
        circle = plt.Circle((x, y), 0.32, fc="#C6F6D5", ec="#276749", lw=1.2)
        ax.add_patch(circle)
        ax.text(x, y, lbl, ha='center', va='center', fontsize=8, fontweight='bold')

    ax.annotate('', xy=(2.68, 2.7), xytext=(1.55, 3.1), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))
    ax.annotate('', xy=(2.68, 2.7), xytext=(1.55, 1.5), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))
    ax.annotate('', xy=(2.68, 1.1), xytext=(1.55, 2.3), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))
    ax.annotate('', xy=(2.68, 1.1), xytext=(1.55, 0.7), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))

    # Layer 3: Normalization (N)
    l3_nodes = [("$N$\n$\\bar{w}_1$", 4.8, 2.7), ("$N$\n$\\bar{w}_2$", 4.8, 1.1)]
    for lbl, x, y in l3_nodes:
        circle = plt.Circle((x, y), 0.32, fc="#FEFCBF", ec="#B7791F", lw=1.2)
        ax.add_patch(circle)
        ax.text(x, y, lbl, ha='center', va='center', fontsize=8, fontweight='bold')

    for x1, y1 in [(3.32, 2.7), (3.32, 1.1)]:
        for x2, y2 in [(4.48, 2.7), (4.48, 1.1)]:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=0.8, color='#718096'))

    # Layer 4: Consequent nodes
    l4_nodes = [("$\\bar{w}_1 f_1$", 6.6, 2.7), ("$\\bar{w}_2 f_2$", 6.6, 1.1)]
    for lbl, x, y in l4_nodes:
        box = patches.FancyBboxPatch((x-0.45, y-0.25), 0.9, 0.5, boxstyle="square,pad=0", fc="#FED7D7", ec="#C53030", lw=1.2)
        ax.add_patch(box)
        ax.text(x, y, lbl, ha='center', va='center', fontsize=8.5, fontweight='bold')

    ax.annotate('', xy=(6.15, 2.7), xytext=(5.12, 2.7), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))
    ax.annotate('', xy=(6.15, 1.1), xytext=(5.12, 1.1), arrowprops=dict(arrowstyle="->", lw=1, color='#4A5568'))

    # Layer 5: Summation node
    circle = plt.Circle((8.4, 1.9), 0.35, fc="#E9D8FD", ec="#6B46C1", lw=1.5)
    ax.add_patch(circle)
    ax.text(8.4, 1.9, "$\sum$\nOutput", ha='center', va='center', fontsize=8.5, fontweight='bold')

    ax.annotate('', xy=(8.05, 1.95), xytext=(7.05, 2.7), arrowprops=dict(arrowstyle="->", lw=1.2, color='#4A5568'))
    ax.annotate('', xy=(8.05, 1.85), xytext=(7.05, 1.1), arrowprops=dict(arrowstyle="->", lw=1.2, color='#4A5568'))

    # Output arrow
    ax.annotate('', xy=(9.6, 1.9), xytext=(8.75, 1.9), arrowprops=dict(arrowstyle="->", lw=2, color='#2B6CB0'))
    ax.text(9.7, 1.9, "$y_{out} = \sum \\bar{w}_i f_i$", va='center', fontsize=10, fontweight='bold', color='#2B6CB0')

    ax.set_xlim(-0.3, 10.8)
    ax.set_ylim(0.2, 4.4)
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/diagram_neuro_fuzzy.png', bbox_inches='tight')
    plt.close()

# 3. CNN Convolution Operation Diagram
def make_convolution_diagram():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8.5, 3.2), dpi=200, gridspec_kw={'width_ratios': [4, 2.5, 3.5]})
    
    # Input feature map (4x4)
    input_mat = np.array([[2, 1, 0, 3],
                          [1, 3, 2, 1],
                          [0, 2, 1, 0],
                          [3, 1, 0, 2]])
    ax1.matshow(input_mat, cmap='Blues', alpha=0.3)
    for i in range(4):
        for j in range(4):
            ax1.text(j, i, str(input_mat[i, j]), ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Highlight top-left 2x2
    rect = patches.Rectangle((-0.5, -0.5), 2, 2, linewidth=2.5, edgecolor='#E53E3E', facecolor='#FEB2B2', alpha=0.4)
    ax1.add_patch(rect)
    ax1.set_xticks(range(4))
    ax1.set_yticks(range(4))
    ax1.set_title("Input Feature Map ($4 \\times 4$)", fontsize=9.5, fontweight='bold', pad=12)

    # Kernel (2x2)
    kernel_mat = np.array([[1, 0],
                           [0, 1]])
    ax2.matshow(kernel_mat, cmap='Reds', alpha=0.3)
    for i in range(2):
        for j in range(2):
            ax2.text(j, i, str(kernel_mat[i, j]), ha='center', va='center', fontsize=12, fontweight='bold', color='#C53030')
    ax2.set_xticks(range(2))
    ax2.set_yticks(range(2))
    ax2.set_title("Filter / Kernel ($2 \\times 2$)", fontsize=9.5, fontweight='bold', pad=12)

    # Output feature map (3x3)
    output_mat = np.array([[5, 3, 1],
                           [3, 4, 2],
                           [1, 2, 3]])
    ax3.matshow(output_mat, cmap='Greens', alpha=0.3)
    for i in range(3):
        for j in range(3):
            col = '#22543D' if (i==0 and j==0) else '#2D3748'
            ax3.text(j, i, str(output_mat[i, j]), ha='center', va='center', fontsize=11, fontweight='bold', color=col)
    
    # Highlight output (0,0) = 5
    rect_out = patches.Rectangle((-0.5, -0.5), 1, 1, linewidth=2.5, edgecolor='#E53E3E', facecolor='#FEB2B2', alpha=0.4)
    ax3.add_patch(rect_out)
    ax3.set_xticks(range(3))
    ax3.set_yticks(range(3))
    ax3.set_title("Output Map ($3 \\times 3$)\n$(2\\times 1 + 1\\times 0 + 1\\times 0 + 3\\times 1 = \\mathbf{5})$", fontsize=8.5, fontweight='bold', pad=12)

    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/diagram_cnn_conv.png', bbox_inches='tight')
    plt.close()

# 4. Neuro-Genetic Hybrid Flowchart
def make_neuro_genetic_diagram():
    fig, ax = plt.subplots(figsize=(8.2, 4.2), dpi=200)
    ax.axis('off')

    boxes = [
        ("Initialize Population\nof Chromosomes\n(Encoded NN Weights / Topology)", 1.5, 3.2, "#EBF8FF", "#3182CE"),
        ("Decode Chromosome\ninto Neural Network Model", 4.5, 3.2, "#FEFCBF", "#D69E2E"),
        ("Train / Forward Pass\non Dataset & Compute Error\n(MSE / Cross-Entropy)", 7.5, 3.2, "#EDF2F7", "#4A5568"),
        ("Evaluate Fitness\n$Fitness = 1 / (1 + MSE)$", 7.5, 1.4, "#FED7D7", "#E53E3E"),
        ("Check Termination\nCriteria\n(Max Gen / Target Fitness)", 4.5, 1.4, "#E2E8F0", "#4A5568"),
        ("Optimal Neural Network\nModel Ready", 1.5, 1.4, "#C6F6D5", "#38A169"),
        ("Apply Genetic Operators\nSelection $\\rightarrow$ Crossover $\\rightarrow$ Mutation", 4.5, -0.2, "#E9D8FD", "#805AD5")
    ]

    for text, x, y, bg, border in boxes:
        box = patches.FancyBboxPatch((x-1.2, y-0.45), 2.4, 0.9, boxstyle="round,pad=0.2", fc=bg, ec=border, lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold', color='#1A202C')

    # Arrows
    ax.annotate('', xy=(3.3, 3.2), xytext=(2.7, 3.2), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2B6CB0'))
    ax.annotate('', xy=(6.3, 3.2), xytext=(5.7, 3.2), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2B6CB0'))
    ax.annotate('', xy=(7.5, 1.85), xytext=(7.5, 2.75), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2B6CB0'))
    ax.annotate('', xy=(5.7, 1.4), xytext=(6.3, 1.4), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2B6CB0'))
    
    # Decision arrows
    ax.annotate('', xy=(2.7, 1.4), xytext=(3.3, 1.4), arrowprops=dict(arrowstyle="->", lw=1.5, color='#38A169'))
    ax.text(3.0, 1.55, "Yes", fontsize=8.5, fontweight='bold', color='#38A169', ha='center')

    ax.annotate('', xy=(4.5, 0.25), xytext=(4.5, 0.95), arrowprops=dict(arrowstyle="->", lw=1.5, color='#E53E3E'))
    ax.text(4.75, 0.6, "No", fontsize=8.5, fontweight='bold', color='#E53E3E')

    # Loop back
    ax.plot([3.3, 1.5, 1.5], [-0.2, -0.2, 2.75], color='#805AD5', lw=1.5, ls='--')
    ax.annotate('', xy=(1.5, 2.75), xytext=(1.5, 2.0), arrowprops=dict(arrowstyle="->", lw=1.5, color='#805AD5', ls='--'))
    ax.text(1.2, 0.8, "Next Gen\nPopulation", fontsize=7.5, fontweight='bold', color='#805AD5', ha='right')

    ax.set_xlim(0, 9)
    ax.set_ylim(-0.8, 4.0)
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/diagram_neuro_genetic.png', bbox_inches='tight')
    plt.close()

# 5. GFRBS Block Diagram
def make_gfrbs_diagram():
    fig, ax = plt.subplots(figsize=(8.2, 3.8), dpi=200)
    ax.axis('off')

    # Outer container for Fuzzy System
    rect_fls = patches.FancyBboxPatch((0.2, 0.5), 5.4, 2.9, boxstyle="round,pad=0.2", fc="#F7FAFC", ec="#A0AEC0", lw=1.5, ls='--')
    ax.add_patch(rect_fls)
    ax.text(2.9, 3.25, "Fuzzy Rule-Based System (FRBS)", fontsize=9, fontweight='bold', color='#4A5568', ha='center')

    # Knowledge Base Box
    rect_kb = patches.FancyBboxPatch((0.5, 1.7), 2.2, 1.3, boxstyle="round,pad=0.1", fc="#EBF8FF", ec="#3182CE", lw=1.2)
    ax.add_patch(rect_kb)
    ax.text(1.6, 2.7, "Knowledge Base (KB)", fontsize=8, fontweight='bold', color='#2B6CB0', ha='center')
    ax.text(1.6, 2.3, "• Data Base (DB)\n(Membership Funcs)", fontsize=7.5, color='#2D3748', ha='center')
    ax.text(1.6, 1.9, "• Rule Base (RB)\n(IF-THEN Rules)", fontsize=7.5, color='#2D3748', ha='center')

    # Inference Engine Box
    rect_ie = patches.FancyBboxPatch((3.2, 1.7), 2.0, 1.3, boxstyle="round,pad=0.1", fc="#FEFCBF", ec="#D69E2E", lw=1.2)
    ax.add_patch(rect_ie)
    ax.text(4.2, 2.5, "Fuzzy Inference\nEngine", fontsize=8.5, fontweight='bold', color='#B7791F', ha='center')
    ax.text(4.2, 1.9, "Fuzzifier $\\rightarrow$ Defuzz", fontsize=7.5, color='#4A5568', ha='center')

    ax.annotate('', xy=(3.2, 2.35), xytext=(2.7, 2.35), arrowprops=dict(arrowstyle="->", lw=1.2, color='#4A5568'))

    # Inputs and Outputs of FRBS
    ax.annotate('', xy=(3.2, 1.9), xytext=(2.7, 1.9), arrowprops=dict(arrowstyle="<-", lw=1.2, color='#4A5568'))
    ax.annotate('', xy=(3.2, 1.0), xytext=(1.0, 1.0), arrowprops=dict(arrowstyle="->", lw=1.2, color='#4A5568'))
    ax.text(0.9, 1.0, "Inputs", fontsize=8.5, fontweight='bold', color='#2D3748', ha='right', va='center')
    ax.text(3.7, 1.0, "Execution / Reasoning", fontsize=7.5, color='#718096', va='center')
    ax.annotate('', xy=(5.2, 1.0), xytext=(4.5, 1.0), arrowprops=dict(arrowstyle="->", lw=1.2, color='#4A5568'))

    # System output
    ax.annotate('', xy=(6.5, 2.35), xytext=(5.2, 2.35), arrowprops=dict(arrowstyle="->", lw=1.2, color='#4A5568'))
    ax.text(6.6, 2.35, "Outputs", fontsize=8.5, fontweight='bold', color='#2D3748', va='center')

    # Genetic Learning Module Box
    rect_ga = patches.FancyBboxPatch((6.2, 0.4), 2.2, 1.6, boxstyle="round,pad=0.1", fc="#FED7D7", ec="#E53E3E", lw=1.5)
    ax.add_patch(rect_ga)
    ax.text(7.3, 1.7, "Genetic Learning\nModule", fontsize=8.5, fontweight='bold', color='#9B2C2C', ha='center')
    ax.text(7.3, 1.15, "• Fitness Evaluation\n• Selection\n• Crossover & Mutation", fontsize=7.5, color='#4A5568', ha='center')
    ax.text(7.3, 0.65, "Michigan / Pittsburgh", fontsize=7, fontweight='bold', color='#C53030', ha='center')

    # Connections to Genetic Module
    ax.annotate('', xy=(7.3, 2.0), xytext=(6.5, 2.35), arrowprops=dict(arrowstyle="->", lw=1.2, color='#C53030', ls='--'))
    ax.text(7.2, 2.25, "Performance\nFeedback", fontsize=7, color='#C53030', ha='center')

    # Feedback to KB
    ax.plot([7.3, 7.3, 1.6, 1.6], [0.4, -0.1, -0.1, 1.7], color='#2B6CB0', lw=1.5, ls='--')
    ax.annotate('', xy=(1.6, 1.7), xytext=(1.6, 1.0), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2B6CB0', ls='--'))
    ax.text(4.4, -0.25, "Evolutionary Optimization of Rules & Membership Parameters", fontsize=7.5, fontweight='bold', color='#2B6CB0', ha='center')

    ax.set_xlim(0, 8.8)
    ax.set_ylim(-0.4, 3.6)
    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/diagram_gfrbs.png', bbox_inches='tight')
    plt.close()

# 6. RNN vs Recursive Diagram
def make_rnn_vs_recursive_diagram():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.4), dpi=200)
    ax1.axis('off')
    ax2.axis('off')

    # Subplot 1: Recurrent Neural Network (Linear Chain)
    ax1.text(2.0, 3.2, "Recurrent Neural Network (RNN)\n(Sequential Temporal Chain)", ha='center', fontsize=9, fontweight='bold', color='#2B6CB0')
    time_steps = [("t-1", 0.6), ("t", 2.0), ("t+1", 3.4)]
    for lbl, x in time_steps:
        # Input x_t
        ax1.text(x, 0.5, f"$x_{{{lbl}}}$", ha='center', va='center', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="circle,pad=0.25", fc="#EDF2F7", ec="#4A5568"))
        # Hidden state h_t
        ax1.text(x, 1.7, f"$h_{{{lbl}}}$", ha='center', va='center', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="circle,pad=0.25", fc="#BEE3F8", ec="#2B6CB0", lw=1.5))
        # Output y_t
        ax1.text(x, 2.7, f"$y_{{{lbl}}}$", ha='center', va='center', fontsize=9, fontweight='bold',
                 bbox=dict(boxstyle="circle,pad=0.25", fc="#C6F6D5", ec="#276749"))

        # Vertical arrows
        ax1.annotate('', xy=(x, 1.45), xytext=(x, 0.75), arrowprops=dict(arrowstyle="->", lw=1.2, color='#4A5568'))
        ax1.annotate('', xy=(x, 2.45), xytext=(x, 1.95), arrowprops=dict(arrowstyle="->", lw=1.2, color='#4A5568'))

    # Recurrent horizontal connections
    ax1.annotate('', xy=(1.75, 1.7), xytext=(0.85, 1.7), arrowprops=dict(arrowstyle="->", lw=1.5, color='#E53E3E'))
    ax1.annotate('', xy=(3.15, 1.7), xytext=(2.25, 1.7), arrowprops=dict(arrowstyle="->", lw=1.5, color='#E53E3E'))
    ax1.text(1.3, 1.85, "$W_{hh}$", fontsize=8, color='#C53030', ha='center')
    ax1.text(2.7, 1.85, "$W_{hh}$", fontsize=8, color='#C53030', ha='center')

    ax1.set_xlim(0, 4.0)
    ax1.set_ylim(0.2, 3.5)

    # Subplot 2: Recursive Neural Network (Hierarchical Tree)
    ax2.text(2.0, 3.2, "Recursive Neural Network\n(Hierarchical Tree Structure)", ha='center', fontsize=9, fontweight='bold', color='#702459')
    
    # Root node (Parent)
    ax2.text(2.0, 2.4, "$h_{root}$", ha='center', va='center', fontsize=9, fontweight='bold',
             bbox=dict(boxstyle="circle,pad=0.25", fc="#FED7D7", ec="#9B2C2C", lw=1.5))
    # Intermediate nodes
    ax2.text(1.2, 1.5, "$h_1$", ha='center', va='center', fontsize=8.5, fontweight='bold',
             bbox=dict(boxstyle="circle,pad=0.25", fc="#FED7E2", ec="#B83280"))
    ax2.text(2.8, 1.5, "$h_2$", ha='center', va='center', fontsize=8.5, fontweight='bold',
             bbox=dict(boxstyle="circle,pad=0.25", fc="#FED7E2", ec="#B83280"))
    # Leaves (Word tokens)
    leaves = [("Word 1", 0.6), ("Word 2", 1.8), ("Word 3", 2.6), ("Word 4", 3.4)]
    for w, x in leaves:
        ax2.text(x, 0.5, w, ha='center', va='center', fontsize=8, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.2", fc="#EDF2F7", ec="#4A5568"))

    # Tree edges
    ax2.annotate('', xy=(1.8, 2.25), xytext=(1.35, 1.7), arrowprops=dict(arrowstyle="->", lw=1.2, color='#702459'))
    ax2.annotate('', xy=(2.2, 2.25), xytext=(2.65, 1.7), arrowprops=dict(arrowstyle="->", lw=1.2, color='#702459'))
    
    ax2.annotate('', xy=(1.1, 1.3), xytext=(0.7, 0.75), arrowprops=dict(arrowstyle="->", lw=1.1, color='#702459'))
    ax2.annotate('', xy=(1.3, 1.3), xytext=(1.7, 0.75), arrowprops=dict(arrowstyle="->", lw=1.1, color='#702459'))
    ax2.annotate('', xy=(2.7, 1.3), xytext=(2.6, 0.75), arrowprops=dict(arrowstyle="->", lw=1.1, color='#702459'))
    ax2.annotate('', xy=(2.9, 1.3), xytext=(3.3, 0.75), arrowprops=dict(arrowstyle="->", lw=1.1, color='#702459'))

    ax2.set_xlim(0.2, 3.8)
    ax2.set_ylim(0.2, 3.5)

    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/diagram_rnn_vs_recursive.png', bbox_inches='tight')
    plt.close()

# 7. Question 13 Pooling Detailed Diagram
def make_q13_pooling_diagram():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(9.0, 3.3), dpi=200, gridspec_kw={'width_ratios': [4, 2.5, 2.5]})

    # Input 4x4 matrix
    input_mat = np.array([[5, 6, 8, 5],
                          [4, 2, 9, 4],
                          [7, 6, 7, 3],
                          [9, 2, 1, 3]])

    # Colors for 4 quadrants
    # Q1 (top-left): light blue
    # Q2 (top-right): light orange
    # Q3 (bottom-left): light green
    # Q4 (bottom-right): light purple
    colors = np.array([
        ['#BEE3F8', '#BEE3F8', '#FEEBC8', '#FEEBC8'],
        ['#BEE3F8', '#BEE3F8', '#FEEBC8', '#FEEBC8'],
        ['#C6F6D5', '#C6F6D5', '#E9D8FD', '#E9D8FD'],
        ['#C6F6D5', '#C6F6D5', '#E9D8FD', '#E9D8FD']
    ])

    ax1.set_xlim(-0.5, 3.5)
    ax1.set_ylim(3.5, -0.5)
    for i in range(4):
        for j in range(4):
            rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, facecolor=colors[i, j], edgecolor='#CBD5E0', lw=1.2)
            ax1.add_patch(rect)
            ax1.text(j, i, str(input_mat[i, j]), ha='center', va='center', fontsize=12, fontweight='bold', color='#1A202C')

    # Bold border around the 4 quadrants
    q_borders = [
        (-0.5, -0.5, '#3182CE'), # Q1
        (1.5, -0.5, '#DD6B20'),  # Q2
        (-0.5, 1.5, '#38A169'),  # Q3
        (1.5, 1.5, '#805AD5')   # Q4
    ]
    for x, y, col in q_borders:
        b_rect = patches.Rectangle((x, y), 2, 2, fill=False, edgecolor=col, lw=2.5)
        ax1.add_patch(b_rect)

    ax1.set_xticks(range(4))
    ax1.set_yticks(range(4))
    ax1.set_title("Input Data ($4 \\times 4$)\nFilter $f=2$, Stride $s=2$", fontsize=9.5, fontweight='bold', pad=10)

    # Max Pooling 2x2
    max_mat = np.array([[6, 9],
                        [9, 7]])
    q_cols = [['#BEE3F8', '#FEEBC8'], ['#C6F6D5', '#E9D8FD']]
    q_border_cols = [['#3182CE', '#DD6B20'], ['#38A169', '#805AD5']]

    ax2.set_xlim(-0.5, 1.5)
    ax2.set_ylim(1.5, -0.5)
    for i in range(2):
        for j in range(2):
            rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, facecolor=q_cols[i][j], edgecolor=q_border_cols[i][j], lw=2.5)
            ax2.add_patch(rect)
            ax2.text(j, i, str(max_mat[i, j]), ha='center', va='center', fontsize=14, fontweight='bold', color='#1A202C')

    ax2.set_xticks(range(2))
    ax2.set_yticks(range(2))
    ax2.set_title("Max-Pooling ($2 \\times 2$)\n$\\max(\\text{quadrant})$", fontsize=9.5, fontweight='bold', pad=10, color='#2B6CB0')

    # Average Pooling 2x2
    avg_mat = np.array([[4.25, 6.50],
                        [6.00, 3.50]])
    ax3.set_xlim(-0.5, 1.5)
    ax3.set_ylim(1.5, -0.5)
    for i in range(2):
        for j in range(2):
            rect = patches.Rectangle((j-0.5, i-0.5), 1, 1, facecolor=q_cols[i][j], edgecolor=q_border_cols[i][j], lw=2.5)
            ax3.add_patch(rect)
            ax3.text(j, i, f"{avg_mat[i, j]:.2f}", ha='center', va='center', fontsize=12, fontweight='bold', color='#1A202C')

    ax3.set_xticks(range(2))
    ax3.set_yticks(range(2))
    ax3.set_title("Average-Pooling ($2 \\times 2$)\n$\\text{mean}(\\text{quadrant})$", fontsize=9.5, fontweight='bold', pad=10, color='#B7791F')

    plt.tight_layout()
    plt.savefig(f'{FIG_DIR}/diagram_pooling_q13.png', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    make_autoencoder_diagram()
    print("Generated Autoencoder diagram.")
    make_anfis_diagram()
    print("Generated ANFIS diagram.")
    make_convolution_diagram()
    print("Generated CNN Convolution diagram.")
    make_neuro_genetic_diagram()
    print("Generated Neuro-Genetic diagram.")
    make_gfrbs_diagram()
    print("Generated GFRBS diagram.")
    make_rnn_vs_recursive_diagram()
    print("Generated RNN vs Recursive diagram.")
    make_q13_pooling_diagram()
    print("Generated Q13 Pooling diagram.")
    print("All diagrams generated successfully in", FIG_DIR)
