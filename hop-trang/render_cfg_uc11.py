import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon

def create_cfg_c1_c2(output_path):
    fig, ax = plt.subplots(figsize=(9, 18), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 205)
    ax.axis('off')

    # Color palette matching UC09 & UC10
    c_blue_face = '#D0E5FF'
    c_blue_edge = '#2B579A'
    c_yellow_face = '#FFF2CC'
    c_yellow_edge = '#D6B656'
    c_pink_face = '#F8CECC'
    c_pink_edge = '#B85450'
    c_purple_face = '#E1D5E7'
    c_purple_edge = '#9673A6'

    def draw_box(x, y, w, h, text, facecolor, edgecolor, shape='round', fontsize=8, bold=True):
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
    draw_box(cx, 196, 28, 4.5, "Start: Dòng 19\nexecute(candidateID, statusData)", c_blue_face, c_blue_edge, shape='round')

    # Node 1 & 2
    draw_box(cx, 183, 28, 7.5, "Node 1:\n!candidateID || !statusData?.status?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.2)
    draw_box(78, 183, 24, 5, "Node 2:\nthrow 'Mã / trạng thái trống'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 3 & 4
    draw_box(cx, 168, 26, 7.5, "Node 3:\n!candidate?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(78, 168, 24, 5, "Node 4:\nthrow 'Ko tìm thấy UV'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 5 & 6
    draw_box(cx, 153, 28, 7.5, "Node 5:\ncurrentStatus === HIRED?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.5)
    draw_box(78, 153, 24, 5, "Node 6:\nthrow 'Hồ sơ đã trúng tuyển'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 7 & 8
    draw_box(cx, 138, 26, 7.5, "Node 7:\n!isAllowedTransition?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.5)
    draw_box(78, 138, 24, 5, "Node 8:\nthrow 'Không được nhảy cóc'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 9 & 10
    draw_box(cx, 123, 28, 7.5, "Node 9:\nREJECTED && !reason?.trim()?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.2)
    draw_box(78, 123, 24, 5, "Node 10:\nthrow 'Thiếu lý do từ chối'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 11 & 12
    draw_box(cx, 108, 28, 7.5, "Node 11:\nREJECTED && reason > 500 ký tự?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.2)
    draw_box(78, 108, 24, 5, "Node 12:\nthrow 'Lý do từ chối > 500 ký tự'", c_pink_face, c_pink_edge, shape='round', fontsize=7.2)

    # Node 13 & 14
    draw_box(cx, 93, 28, 7.5, "Node 13:\nREJECTED->SCREENING && !reason?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7)
    draw_box(78, 93, 24, 5, "Node 14:\nthrow 'Thiếu lý do khôi phục'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 15 (Process)
    draw_box(cx, 76, 32, 6.5, "Node 15:\ncandidateRepo.updateStatus()\ncandidate.updateStatus(newStatus)", c_purple_face, c_purple_edge, shape='round', fontsize=7.5)

    # Node 16a & 16b (Try / Catch)
    draw_box(cx, 58, 28, 6.5, "Node 16a (Try):\nmailSvc.sendEmail(thông báo)", c_purple_face, c_purple_edge, shape='round', fontsize=7.5)
    draw_box(78, 58, 24, 5.5, "Node 16b (Catch):\nconsole.warn('Lỗi email')", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 17
    draw_box(cx, 40, 32, 6.5, "Node 17:\nresult = { success: true, ... }", c_purple_face, c_purple_edge, shape='round', fontsize=7.5)

    # Node 18 (Return)
    draw_box(cx, 22, 28, 5, "Node 18 (Return Success):\nreturn result", c_blue_face, c_blue_edge, shape='round', fontsize=8)

    # Exit summary node (End)
    draw_box(78, 22, 22, 5, "End: Kết thúc hàm", c_blue_face, c_blue_edge, shape='round', fontsize=8)

    # Arrows
    draw_arrow(cx, 193.75, cx, 186.75)
    
    # 1 -> 2 (True) & 1 -> 3 (False)
    draw_arrow(cx + 14, 183, 66, 183, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 179.25, cx, 171.75, label='False', label_offset=(3.5, 0))

    # 3 -> 4 (True) & 3 -> 5 (False)
    draw_arrow(cx + 13, 168, 66, 168, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 164.25, cx, 156.75, label='False', label_offset=(3.5, 0))

    # 5 -> 6 (True) & 5 -> 7 (False)
    draw_arrow(cx + 14, 153, 66, 153, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 149.25, cx, 141.75, label='False', label_offset=(3.5, 0))

    # 7 -> 8 (True) & 7 -> 9 (False)
    draw_arrow(cx + 13, 138, 66, 138, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 134.25, cx, 126.75, label='False', label_offset=(3.5, 0))

    # 9 -> 10 (True) & 9 -> 11 (False)
    draw_arrow(cx + 14, 123, 66, 123, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 119.25, cx, 111.75, label='False', label_offset=(3.5, 0))

    # 11 -> 12 (True) & 11 -> 13 (False)
    draw_arrow(cx + 14, 108, 66, 108, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 104.25, cx, 96.75, label='False', label_offset=(3.5, 0))

    # 13 -> 14 (True) & 13 -> 15 (False)
    draw_arrow(cx + 14, 93, 66, 93, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 89.25, cx, 79.25, label='False', label_offset=(3.5, 0))

    # 15 -> 16a
    draw_arrow(cx, 72.75, cx, 61.25)

    # 16a -> 16b (Catch) & 16a -> 17 (Try OK)
    draw_arrow(cx + 14, 58, 66, 58, label='Ngoại lệ', label_offset=(0, 1.5))
    draw_arrow(cx, 54.75, cx, 43.25, label='Thành công', label_offset=(5.5, 0))

    # 16b -> 17
    draw_elbow_arrow([(78, 55.25), (78, 40), (cx + 16, 40)], label='Tiếp tục', label_idx=1, label_offset=(4, 1.5))

    # 17 -> 18
    draw_arrow(cx, 36.75, cx, 24.5)

    # Connect exits to End
    draw_arrow(cx + 14, 22, 67, 22)
    draw_elbow_arrow([(90, 183), (95, 183), (95, 24.5), (89, 24.5)])

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"CFG C1/C2 UC11 saved to {output_path}")

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

    def draw_box(x, y, w, h, text, facecolor, edgecolor, shape='round', fontsize=8, bold=True):
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
    draw_box(cx, 207, 28, 4.5, "Start: Dòng 19\nexecute(candidateID, statusData)", c_blue_face, c_blue_edge, shape='round')

    # Node 1a & 1b (C3 Split)
    draw_box(cx, 195, 26, 6.5, "Node 1a:\n!candidateID?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.5)
    draw_box(cx, 180, 26, 6.5, "Node 1b:\n!statusData?.status?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.2)
    draw_box(78, 188, 24, 6, "Node 2:\nthrow 'Mã / trạng thái trống'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 3 & 4
    draw_box(cx, 166, 26, 7.5, "Node 3:\n!candidate?", c_yellow_face, c_yellow_edge, shape='diamond')
    draw_box(78, 166, 24, 5, "Node 4:\nthrow 'Ko tìm thấy UV'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 5 & 6
    draw_box(cx, 151, 28, 7.5, "Node 5:\ncurrentStatus === HIRED?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.5)
    draw_box(78, 151, 24, 5, "Node 6:\nthrow 'Hồ sơ đã trúng tuyển'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 7 & 8
    draw_box(cx, 136, 26, 7.5, "Node 7:\n!isAllowedTransition?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.5)
    draw_box(78, 136, 24, 5, "Node 8:\nthrow 'Không được nhảy cóc'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 9 & 10
    draw_box(cx, 121, 28, 7.5, "Node 9:\nREJECTED && !reason?.trim()?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.2)
    draw_box(78, 121, 24, 5, "Node 10:\nthrow 'Thiếu lý do từ chối'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 11 & 12
    draw_box(cx, 106, 28, 7.5, "Node 11:\nREJECTED && reason > 500 ký tự?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7.2)
    draw_box(78, 106, 24, 5, "Node 12:\nthrow 'Lý do từ chối > 500 ký tự'", c_pink_face, c_pink_edge, shape='round', fontsize=7.2)

    # Node 13 & 14
    draw_box(cx, 91, 28, 7.5, "Node 13:\nREJECTED->SCREENING && !reason?", c_yellow_face, c_yellow_edge, shape='diamond', fontsize=7)
    draw_box(78, 91, 24, 5, "Node 14:\nthrow 'Thiếu lý do khôi phục'", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 15 (Process)
    draw_box(cx, 74, 32, 6.5, "Node 15:\ncandidateRepo.updateStatus()\ncandidate.updateStatus(newStatus)", c_purple_face, c_purple_edge, shape='round', fontsize=7.5)

    # Node 16a & 16b (Try / Catch)
    draw_box(cx, 56, 28, 6.5, "Node 16a (Try):\nmailSvc.sendEmail(thông báo)", c_purple_face, c_purple_edge, shape='round', fontsize=7.5)
    draw_box(78, 56, 24, 5.5, "Node 16b (Catch):\nconsole.warn('Lỗi email')", c_pink_face, c_pink_edge, shape='round', fontsize=7.5)

    # Node 17
    draw_box(cx, 38, 32, 6.5, "Node 17:\nresult = { success: true, ... }", c_purple_face, c_purple_edge, shape='round', fontsize=7.5)

    # Node 18 (Return)
    draw_box(cx, 20, 28, 5, "Node 18 (Return Success):\nreturn result", c_blue_face, c_blue_edge, shape='round', fontsize=8)

    # Exit summary node (End)
    draw_box(78, 20, 22, 5, "End: Kết thúc hàm", c_blue_face, c_blue_edge, shape='round', fontsize=8)

    # Arrows
    draw_arrow(cx, 204.75, cx, 198.25)
    
    # 1a -> 2 (True - short circuit) & 1a -> 1b (False)
    draw_elbow_arrow([(cx + 13, 195), (66, 195), (66, 189)], label='True (Ngắt mạch)', label_offset=(0, 2))
    draw_arrow(cx, 191.75, cx, 183.25, label='False', label_offset=(3.5, 0))

    # 1b -> 2 (True) & 1b -> 3 (False)
    draw_elbow_arrow([(cx + 13, 180), (66, 180), (66, 186.5)], label='True', label_offset=(0, 2))
    draw_arrow(cx, 176.75, cx, 169.75, label='False', label_offset=(3.5, 0))

    # 3 -> 4 & 3 -> 5
    draw_arrow(cx + 13, 166, 66, 166, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 162.25, cx, 154.75, label='False', label_offset=(3.5, 0))

    # 5 -> 6 & 5 -> 7
    draw_arrow(cx + 14, 151, 66, 151, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 147.25, cx, 139.75, label='False', label_offset=(3.5, 0))

    # 7 -> 8 & 7 -> 9
    draw_arrow(cx + 13, 136, 66, 136, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 132.25, cx, 124.75, label='False', label_offset=(3.5, 0))

    # 9 -> 10 & 9 -> 11
    draw_arrow(cx + 14, 121, 66, 121, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 117.25, cx, 109.75, label='False', label_offset=(3.5, 0))

    # 11 -> 12 & 11 -> 13
    draw_arrow(cx + 14, 106, 66, 106, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 102.25, cx, 94.75, label='False', label_offset=(3.5, 0))

    # 13 -> 14 & 13 -> 15
    draw_arrow(cx + 14, 91, 66, 91, label='True', label_offset=(0, 1.5))
    draw_arrow(cx, 87.25, cx, 77.25, label='False', label_offset=(3.5, 0))

    # 15 -> 16a
    draw_arrow(cx, 70.75, cx, 59.25)

    # 16a -> 16b & 16a -> 17
    draw_arrow(cx + 14, 56, 66, 56, label='Ngoại lệ', label_offset=(0, 1.5))
    draw_arrow(cx, 52.75, cx, 41.25, label='Thành công', label_offset=(5.5, 0))

    # 16b -> 17
    draw_elbow_arrow([(78, 53.25), (78, 38), (cx + 16, 38)], label='Tiếp tục', label_idx=1, label_offset=(4, 1.5))

    # 17 -> 18
    draw_arrow(cx, 34.75, cx, 22.5)

    # Connect exits to End
    draw_arrow(cx + 14, 20, 67, 20)
    draw_elbow_arrow([(90, 188), (95, 188), (95, 22.5), (89, 22.5)])

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"CFG C3 UC11 saved to {output_path}")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.abspath(__file__))
    c1_c2_path = os.path.join(base_dir, 'cfg_uc11_c1_c2.png')
    c3_path = os.path.join(base_dir, 'cfg_uc11_c3.png')
    create_cfg_c1_c2(c1_c2_path)
    create_cfg_c3(c3_path)
