import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
import os

def create_cfg_c1_c2(output_path):
    fig, ax = plt.subplots(figsize=(9, 18), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 205)
    ax.axis('off')

    c_blue_face = '#D0E5FF'
    c_blue_edge = '#2B579A'
    c_yellow_face = '#FFF2CC'
    c_yellow_edge = '#D6B656'
    c_pink_face = '#F8CECC'
    c_pink_edge = '#B85450'
    c_purple_face = '#E1D5E7'
    c_purple_edge = '#9673A6'

    def draw_box(x, y, w, h, text, facecolor, edgecolor, shape='round', fontsize=8.5, bold=True):
        if shape == 'round':
            box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                 boxstyle="round,pad=0.6,rounding_size=1.5",
                                 facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5)
            ax.add_patch(box)
        elif shape == 'diamond':
            pts = [[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]]
            poly = Polygon(pts, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5)
            ax.add_patch(poly)
        
        weight = 'bold' if bold else 'normal'
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight=weight,
                color='#111111')

    def draw_arrow(x1, y1, x2, y2, label=None, label_offset=(0, 0)):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor='#333333', edgecolor='#333333',
                                    arrowstyle='->', lw=1.2, shrinkA=0, shrinkB=0))
        if label:
            mx = (x1 + x2) / 2 + label_offset[0]
            my = (y1 + y2) / 2 + label_offset[1]
            ax.text(mx, my, label, fontsize=8, fontweight='bold', color='#222222',
                    bbox=dict(facecolor='white', edgecolor='none', pad=1))

    def draw_elbow_arrow(pts, label=None, label_idx=0, label_offset=(0, 0)):
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i+1]
            is_last = (i == len(pts) - 2)
            if is_last:
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                            arrowprops=dict(facecolor='#333333', edgecolor='#333333',
                                            arrowstyle='->', lw=1.2, shrinkA=0, shrinkB=0))
            else:
                ax.plot([x1, x2], [y1, y2], color='#333333', lw=1.2)
            
            if label and i == label_idx:
                mx = (x1 + x2) / 2 + label_offset[0]
                my = (y1 + y2) / 2 + label_offset[1]
                ax.text(mx, my, label, fontsize=8, fontweight='bold', color='#222222',
                        bbox=dict(facecolor='white', edgecolor='none', pad=1))

    cx = 38

    # Start
    draw_box(cx, 198, 26, 4.5, "Bắt đầu: execute(input)", c_blue_face, c_blue_edge, shape='round')

    # Node 1
    draw_box(cx, 184, 28, 8, "Node 1:\n!candidateIds || len == 0?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(78, 184, 24, 5, "Node 2:\nthrow 'Danh sách trống'", c_pink_face, c_pink_edge, shape='round')

    # Node 3
    draw_box(cx, 169, 26, 7.5, "Node 3:\n!title?.trim()?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(78, 169, 24, 5, "Node 4:\nthrow 'Tiêu đề trống'", c_pink_face, c_pink_edge, shape='round')

    # Node 5
    draw_box(cx, 154, 26, 7.5, "Node 5:\n!content?.trim()?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(78, 154, 24, 5, "Node 6:\nthrow 'Nội dung trống'", c_pink_face, c_pink_edge, shape='round')

    # Node 7
    draw_box(cx, 140, 32, 5.5, "Node 7:\nfailed=[], totalSent=0, Promise.all", c_purple_face, c_purple_edge, shape='round', fontsize=8)

    # Node 8
    draw_box(cx, 126, 28, 8, "Node 8:\nfor (i < candidates.length)?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=8)

    # Node 9
    draw_box(cx, 110, 24, 7.5, "Node 9:\n!candidate?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(16, 110, 18, 5, "Node 10:\nfailed.push & cont.", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 11
    draw_box(cx, 96, 24, 7.5, "Node 11:\n!personal?.email?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(16, 96, 18, 5, "Node 12:\nfailed.push & cont.", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 13
    draw_box(cx, 82, 24, 7.5, "Node 13:\nif (jobID)?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(76, 82, 24, 5.5, "Node 14a (Try):\njobRepo.getById(jobID)", c_purple_face, c_purple_edge, shape='round', fontsize=7.5)
    draw_box(76, 71, 24, 5, "Node 14b (Catch):\nconsole.warn(Lỗi Job)", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 15
    draw_box(cx, 63, 30, 6, "Node 15:\nreplacePlaceholders & sendEmail", c_purple_face, c_purple_edge, shape='round', fontsize=8)

    # Node 16
    draw_box(cx, 49, 24, 7.5, "Node 16:\nif (sent)?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(20, 39, 18, 5, "Node 17:\ntotalSent++", c_purple_face, c_purple_edge, shape='round', fontsize=8)
    draw_box(60, 39, 22, 5, "Node 18:\nfailed.push('Lỗi mail')", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 19
    draw_box(86, 53, 22, 5.5, "Node 19 (Catch ngoài):\ncatch(error) -> failed.push", c_pink_face, c_pink_edge, shape='round', fontsize=7)

    # Node 20
    draw_box(86, 126, 22, 6, "Node 20:\nreturn { success: true }", c_blue_face, c_blue_edge, shape='round', fontsize=8)

    # Arrows
    draw_arrow(cx, 195.75, cx, 188)
    draw_arrow(cx + 14, 184, 66, 184, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 180, cx, 172.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx + 13, 169, 66, 169, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 165.25, cx, 157.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx + 13, 154, 66, 154, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 150.25, cx, 142.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx, 137.25, cx, 130)

    draw_arrow(cx + 14, 126, 75, 126, label='False (Hết ds)', label_offset=(0, 1.5))
    draw_arrow(cx, 122, cx, 113.75, label='True', label_offset=(3.5, 0))

    draw_arrow(cx - 12, 110, 25, 110, label='True', label_offset=(0, 1.5))
    draw_elbow_arrow([(16, 112.5), (16, 130), (cx - 2, 130), (cx - 2, 127)])
    draw_arrow(cx, 106.25, cx, 99.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx - 12, 96, 25, 96, label='True', label_offset=(0, 1.5))
    draw_elbow_arrow([(7, 96), (7, 128), (cx - 4, 128), (cx - 4, 127)])
    draw_arrow(cx, 92.25, cx, 85.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx + 12, 82, 64, 82, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 78.25, cx, 66, label='False', label_offset=(3.5, 0))

    draw_arrow(76, 79.25, 76, 73.5, label='Lỗi', label_offset=(2.5, 0))
    draw_elbow_arrow([(64, 80.5), (57, 80.5), (57, 64.5), (53, 64.5)], label='Thành công', label_idx=1, label_offset=(-5.5, 0))
    draw_elbow_arrow([(64, 71), (55, 71), (55, 62), (53, 62)])

    draw_arrow(cx, 60, cx, 52.75)

    draw_elbow_arrow([(cx - 12, 49), (20, 49), (20, 41.5)], label='True', label_offset=(-1, 1.5))
    draw_elbow_arrow([(cx + 12, 49), (60, 49), (60, 41.5)], label='False', label_offset=(1, 1.5))

    draw_elbow_arrow([(20, 36.5), (20, 28), (4, 28), (4, 126), (cx - 14, 126)])
    draw_elbow_arrow([(60, 36.5), (60, 26), (2, 26), (2, 124), (cx - 14, 124)])

    draw_elbow_arrow([(53, 63), (86, 63), (86, 56)], label='Exception', label_offset=(-5, 1.5))
    draw_elbow_arrow([(86, 50.25), (86, 24), (0, 24), (0, 122), (cx - 14, 122)])

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"CFG C1/C2 saved to {output_path}")

def create_cfg_c3(output_path):
    fig, ax = plt.subplots(figsize=(9, 19), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 215)
    ax.axis('off')

    c_blue_face = '#D0E5FF'
    c_blue_edge = '#2B579A'
    c_yellow_face = '#FFF2CC'
    c_yellow_edge = '#D6B656'
    c_pink_face = '#F8CECC'
    c_pink_edge = '#B85450'
    c_purple_face = '#E1D5E7'
    c_purple_edge = '#9673A6'

    def draw_box(x, y, w, h, text, facecolor, edgecolor, shape='round', fontsize=8.5, bold=True):
        if shape == 'round':
            box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                 boxstyle="round,pad=0.6,rounding_size=1.5",
                                 facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5)
            ax.add_patch(box)
        elif shape == 'diamond':
            pts = [[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]]
            poly = Polygon(pts, facecolor=facecolor, edgecolor=edgecolor, linewidth=1.5)
            ax.add_patch(poly)
        
        weight = 'bold' if bold else 'normal'
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, fontweight=weight,
                color='#111111')

    def draw_arrow(x1, y1, x2, y2, label=None, label_offset=(0, 0)):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor='#333333', edgecolor='#333333',
                                    arrowstyle='->', lw=1.2, shrinkA=0, shrinkB=0))
        if label:
            mx = (x1 + x2) / 2 + label_offset[0]
            my = (y1 + y2) / 2 + label_offset[1]
            ax.text(mx, my, label, fontsize=8, fontweight='bold', color='#222222',
                    bbox=dict(facecolor='white', edgecolor='none', pad=1))

    def draw_elbow_arrow(pts, label=None, label_idx=0, label_offset=(0, 0)):
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i+1]
            is_last = (i == len(pts) - 2)
            if is_last:
                ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                            arrowprops=dict(facecolor='#333333', edgecolor='#333333',
                                            arrowstyle='->', lw=1.2, shrinkA=0, shrinkB=0))
            else:
                ax.plot([x1, x2], [y1, y2], color='#333333', lw=1.2)
            
            if label and i == label_idx:
                mx = (x1 + x2) / 2 + label_offset[0]
                my = (y1 + y2) / 2 + label_offset[1]
                ax.text(mx, my, label, fontsize=8, fontweight='bold', color='#222222',
                        bbox=dict(facecolor='white', edgecolor='none', pad=1))

    cx = 38

    # Start
    draw_box(cx, 206, 26, 4.5, "Bắt đầu: execute(input)", c_blue_face, c_blue_edge, shape='round')

    # Node 1a & Node 1b (C3 Split)
    draw_box(cx, 194, 28, 7.5, "Node 1a:\n!candidateIds?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(cx, 180, 28, 7.5, "Node 1b:\ncandidateIds.length == 0?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.5)
    draw_box(78, 187, 24, 5.5, "Node 2:\nthrow 'Danh sách trống'", c_pink_face, c_pink_edge, shape='round')

    # Node 3
    draw_box(cx, 166, 26, 7.5, "Node 3:\n!title?.trim()?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(78, 166, 24, 5, "Node 4:\nthrow 'Tiêu đề trống'", c_pink_face, c_pink_edge, shape='round')

    # Node 5
    draw_box(cx, 152, 26, 7.5, "Node 5:\n!content?.trim()?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(78, 152, 24, 5, "Node 6:\nthrow 'Nội dung trống'", c_pink_face, c_pink_edge, shape='round')

    # Node 7
    draw_box(cx, 138, 32, 5.5, "Node 7:\nfailed=[], totalSent=0, Promise.all", c_purple_face, c_purple_edge, shape='round', fontsize=8)

    # Node 8
    draw_box(cx, 124, 28, 8, "Node 8:\nfor (i < candidates.length)?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=8)

    # Node 9
    draw_box(cx, 108, 24, 7.5, "Node 9:\n!candidate?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(16, 108, 18, 5, "Node 10:\nfailed.push & cont.", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 11
    draw_box(cx, 94, 24, 7.5, "Node 11:\n!personal?.email?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(16, 94, 18, 5, "Node 12:\nfailed.push & cont.", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 13
    draw_box(cx, 80, 24, 7.5, "Node 13:\nif (jobID)?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(76, 80, 24, 5.5, "Node 14a (Try):\njobRepo.getById(jobID)", c_purple_face, c_purple_edge, shape='round', fontsize=7.5)
    draw_box(76, 69, 24, 5, "Node 14b (Catch):\nconsole.warn(Lỗi Job)", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 15
    draw_box(cx, 61, 30, 6, "Node 15:\nreplacePlaceholders & sendEmail", c_purple_face, c_purple_edge, shape='round', fontsize=8)

    # Node 16
    draw_box(cx, 47, 24, 7.5, "Node 16:\nif (sent)?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(20, 37, 18, 5, "Node 17:\ntotalSent++", c_purple_face, c_purple_edge, shape='round', fontsize=8)
    draw_box(60, 37, 22, 5, "Node 18:\nfailed.push('Lỗi mail')", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 19
    draw_box(86, 51, 22, 5.5, "Node 19 (Catch ngoài):\ncatch(error) -> failed.push", c_pink_face, c_pink_edge, shape='round', fontsize=7)

    # Node 20
    draw_box(86, 124, 22, 6, "Node 20:\nreturn { success: true }", c_blue_face, c_blue_edge, shape='round', fontsize=8)

    # Arrows
    draw_arrow(cx, 203.75, cx, 197.75)

    draw_elbow_arrow([(cx + 14, 194), (66, 194), (66, 188), (78 - 12, 188)], label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 190.25, cx, 183.75, label='False', label_offset=(3.5, 0))

    draw_elbow_arrow([(cx + 14, 180), (66, 180), (66, 186), (78 - 12, 186)], label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 176.25, cx, 169.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx + 13, 166, 66, 166, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 162.25, cx, 155.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx + 13, 152, 66, 152, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 148.25, cx, 140.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx, 135.25, cx, 128)

    draw_arrow(cx + 14, 124, 75, 124, label='False (Hết ds)', label_offset=(0, 1.5))
    draw_arrow(cx, 120, cx, 111.75, label='True', label_offset=(3.5, 0))

    draw_arrow(cx - 12, 108, 25, 108, label='True', label_offset=(0, 1.5))
    draw_elbow_arrow([(16, 110.5), (16, 128), (cx - 2, 128), (cx - 2, 125)])
    draw_arrow(cx, 104.25, cx, 97.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx - 12, 94, 25, 94, label='True', label_offset=(0, 1.5))
    draw_elbow_arrow([(7, 94), (7, 126), (cx - 4, 126), (cx - 4, 125)])
    draw_arrow(cx, 90.25, cx, 83.75, label='False', label_offset=(3.5, 0))

    draw_arrow(cx + 12, 80, 64, 80, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 76.25, cx, 64, label='False', label_offset=(3.5, 0))

    draw_arrow(76, 77.25, 76, 71.5, label='Lỗi', label_offset=(2.5, 0))
    draw_elbow_arrow([(64, 78.5), (57, 78.5), (57, 62.5), (53, 62.5)], label='Thành công', label_idx=1, label_offset=(-5.5, 0))
    draw_elbow_arrow([(64, 69), (55, 69), (55, 60), (53, 60)])

    draw_arrow(cx, 58, cx, 50.75)

    draw_elbow_arrow([(cx - 12, 47), (20, 47), (20, 39.5)], label='True', label_offset=(-1, 1.5))
    draw_elbow_arrow([(cx + 12, 47), (60, 47), (60, 39.5)], label='False', label_offset=(1, 1.5))

    draw_elbow_arrow([(20, 34.5), (20, 28), (4, 28), (4, 124), (cx - 14, 124)])
    draw_elbow_arrow([(60, 34.5), (60, 26), (2, 26), (2, 122), (cx - 14, 122)])

    draw_elbow_arrow([(53, 61), (86, 61), (86, 54)], label='Exception', label_offset=(-5, 1.5))
    draw_elbow_arrow([(86, 48.25), (86, 24), (0, 24), (0, 120), (cx - 14, 120)])

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"CFG C3 saved to {output_path}")

if __name__ == '__main__':
    base_dir = r'd:\test\cse462-testing\hop-trang'
    create_cfg_c1_c2(os.path.join(base_dir, 'cfg_uc09_c1_c2.png'))
    create_cfg_c3(os.path.join(base_dir, 'cfg_uc09_c3.png'))
