import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_er_diagram(filename='Project-Report/er_diagram.png'):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Entities with positions and fields
    entities = {
        'Department': (0.8, 6.0, ['dept_id (PK)', 'dept_name (UQ)', 'hod_name']),
        'Student': (0.8, 2.5, ['student_id (PK)', 'name', 'dept_id (FK)', 'cgpa', 'email (UQ)']),
        'Company': (8.8, 6.0, ['company_id (PK)', 'name', 'sector', 'hr_contact']),
        'Drive': (8.8, 2.5, ['drive_id (PK)', 'company_id (FK)', 'role', 'ctc', 'drive_date', 'min_cgpa']),
        'Application': (4.8, 4.0, ['application_id (PK)', 'student_id (FK)', 'drive_id (FK)', 'status (ENUM)']),
        'Interview': (3.0, 0.5, ['interview_id (PK)', 'application_id (FK)', 'round_no', 'result (ENUM)']),
        'Placement': (6.6, 0.5, ['placement_id (PK)', 'application_id (FK, UQ)', 'package', 'placement_date'])
    }

    boxes = {}
    for name, (x, y, fields) in entities.items():
        w = 2.4
        h = 0.35 + len(fields) * 0.25
        # Box background
        rect = patches.FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.08", 
                                      ec="#166e58", fc="#f4f9f6", lw=1.5)
        ax.add_patch(rect)
        # Header bar
        header = patches.FancyBboxPatch((x, y - 0.35), w, 0.35, boxstyle="round,pad=0.04", 
                                        ec="#166e58", fc="#166e58", lw=1.5)
        ax.add_patch(header)
        ax.text(x + w/2, y - 0.22, name, color="white", fontsize=10, weight="bold", ha="center", va="center")
        
        # Fields
        for i, f in enumerate(fields):
            weight = "bold" if "PK" in f else "normal"
            color = "#0f3d32" if "PK" in f or "FK" in f else "#333333"
            ax.text(x + 0.12, y - 0.55 - i * 0.25, f, color=color, fontsize=8, weight=weight, va="center")
        
        boxes[name] = (x, y, w, h)

    # Connecting lines with cardinalities
    connections = [
        ('Department', 'Student', (2.0, 5.0), (2.0, 3.8), '1', 'N'),
        ('Company', 'Drive', (10.0, 5.0), (10.0, 4.0), '1', 'N'),
        ('Student', 'Application', (3.2, 2.5), (4.8, 4.0), '1', 'N'),
        ('Drive', 'Application', (8.8, 2.5), (7.2, 4.0), '1', 'N'),
        ('Application', 'Interview', (5.5, 2.8), (4.2, 1.4), '1', 'N'),
        ('Application', 'Placement', (6.5, 2.8), (7.5, 1.4), '1', '1')
    ]

    for e1, e2, p1, p2, c1, c2 in connections:
        ax.annotate('', xy=p2, xytext=p1,
                    arrowprops=dict(arrowstyle="->", color="#166e58", lw=1.5, ls="--"))
        ax.text(p1[0] + 0.1, p1[1] - 0.1, c1, color="#e65100", fontsize=9, weight="bold")
        ax.text(p2[0] - 0.1, p2[1] + 0.1, c2, color="#e65100", fontsize=9, weight="bold")

    plt.title("Entity-Relationship (ER) Schema - Campus Placement Management System", 
              fontsize=13, weight="bold", color="#166e58", pad=20)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    draw_er_diagram()
    print("ER diagram generated.")
