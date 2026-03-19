# -*- coding: utf-8 -*-
"""Build 40 compact session plans and replace in lessonplan.html"""
import re

LP = r"c:\wamp64\www\ICTNOTES\LEVEL05\Version02\K72t001m01\lessonplan.html"

# 40 chapters: title, hours (total 90: 30*2 + 10*3)
SESSIONS = [
    ("Ch 1: Identify solution range and contractual scope", 2),
    ("Ch 2: Outline proposed solution within scope", 2),
    ("Ch 3: Identify and agree key stakeholders", 2),
    ("Ch 4: Stakeholder roles and agreement process", 2),
    ("Ch 5: Plan time schedule", 2),
    ("Ch 6: Arrange meetings and follow organizational standards", 2),
    ("Ch 7: Practical – Solution range and scope", 2),
    ("Ch 8: Practical – Stakeholder identification", 2),
    ("Ch 9: Practical – Schedule and meeting arrangement", 2),
    ("Ch 10: Consolidation – Element 1", 1),
    ("Ch 11: Data gathering techniques", 2),
    ("Ch 12: Identify requirements through data gathering", 3),
    ("Ch 13: Recognize present workflow", 2),
    ("Ch 14: Observe existing processes", 2),
    ("Ch 15: Identify source documents from present system", 3),
    ("Ch 16: Record key decisions from client meetings", 3),
    ("Ch 17: Practical – Data gathering application", 2),
    ("Ch 18: Practical – Workflow observation and documentation", 2),
    ("Ch 19: Practical – Source document identification", 1),
    ("Ch 20: Consolidation – Element 2", 1),
    ("Ch 21: Document requirement specifications", 3),
    ("Ch 22: Structure and format of specifications", 3),
    ("Ch 23: Functional and non-functional requirements", 2),
    ("Ch 24: Highlight functional/non-functional requirements", 2),
    ("Ch 25: Suggested business process improvements", 2),
    ("Ch 26: Practical – Requirement specification documentation", 2),
    ("Ch 27: Practical – Client meeting recording", 2),
    ("Ch 28: Consolidation – Element 3", 1),
    ("Ch 29: Present requirement specifications to client", 2),
    ("Ch 30: Explain requirement specifications", 2),
    ("Ch 31: Develop prototypes", 3),
    ("Ch 32: Present prototypes", 3),
    ("Ch 33: Obtain client confirmation for requirement specification", 2),
    ("Ch 34: Practical – Presentation and prototype development", 2),
    ("Ch 35: Practical – Client confirmation process", 2),
    ("Ch 36: Consolidation – Element 4", 1),
    ("Ch 37: Conduct feasibility study – technical and economic", 2),
    ("Ch 38: Feasibility – practical, organizational, legal", 2),
    ("Ch 39: Feasibility study report structure", 2),
    ("Ch 40: Practical – Feasibility study report preparation", 4),
]

def session_block(n, title, hrs):
    return '''
      <div class="session-title">''' + title + ''' (''' + str(hrs) + ''' h)</div>
      <div class="table-wrapper">
        <table class="table table-bordered table-sm">
          <tr><th style="width:20%;">Objectives</th><td>Cover key learning points for this chapter</td></tr>
          <tr><th>Methods</th><td>Lecture, discussion, practical as applicable</td></tr>
          <tr><th>Assessment</th><td>Ass-st-''' + str((n-1)//4 + 1).zfill(2) + '''</td></tr>
        </table>
      </div>
      <div class="table-wrapper">
        <table class="table table-bordered table-sm">
          <thead><tr><th>Time</th><th>Phase</th><th>Activity</th></tr></thead>
          <tbody>
            <tr><td>15 min</td><td><span class="phase-badge phase-intro">Intro</span></td><td>Recall and introduce topic</td></tr>
            <tr><td>''' + str(hrs*60 - 30) + ''' min</td><td><span class="phase-badge phase-dev">Development</span></td><td>Teach and practice</td></tr>
            <tr><td>15 min</td><td><span class="phase-badge phase-cons">Consolidation</span></td><td>Summary and check</td></tr>
          </tbody>
        </table>
      </div>'''

def main():
    with open(LP, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = '      <h3 class="mt-5"><i class="fas fa-calendar-alt text-primary"></i> Session Plans</h3>'
    end_marker = '\n    <!-- Practical Assignments -->'
    # From start_marker through the content-card's closing </div> (before Practical Assignments)
    pattern = re.escape(start_marker) + r'.*?' + re.escape(end_marker)
    # We need to replace including the closing </div> that belongs to content-card. So the regex should stop at "    </div>\n\n    <!-- Practical"
    pattern2 = start_marker + r'[\s\S]*?(?=    <!-- Practical Assignments -->)'

    new_sections = []
    new_sections.append('      <h3 class="mt-5"><i class="fas fa-calendar-alt text-primary"></i> Session Plans (40 Chapters)</h3>\n')
    for i, (title, hrs) in enumerate(SESSIONS, 1):
        new_sections.append(session_block(i, title, hrs))
    new_content_block = ''.join(new_sections)

    # Replace: from "Session Plans</h3>" through the last "</div>" before "<!-- Practical Assignments -->"
    idx_start = content.find(start_marker)
    idx_end = content.find('    <!-- Practical Assignments -->')
    if idx_start == -1 or idx_end == -1:
        print("Markers not found", idx_start, idx_end)
        return
    # Include the closing </div> of the content-card (there are two </div> before Practical - one for inner wrapper, one for content-card)
    before = content[:idx_start]
    after = content[idx_end:]  # "    <!-- Practical Assignments -->" ...
    new_full = before + new_content_block + "\n\n    " + "</div>\n\n    " + after
    # We added one "</div>" - but the original had two </div> before <!-- Practical. So after our new_content_block we need "\n\n    </div>\n\n    </div>\n\n    <!-- Practical..."
    # Check original structure: ... </table> </div> </div> </div> <!-- Practical
    snippet = content[idx_end-200:idx_end]
    # So we need to preserve the two closing </div>s. So after = "    </div>\n\n    </div>\n\n    <!-- Practical..."
    # So we should not add an extra </div>. Our new_content_block doesn't close the content-card. So we need: new_content_block + the two "</div>" that were there. So find how many </div> are between end of session content and "<!-- Practical"
    tail = content[idx_start:idx_end]
    n_close = tail.count('</div>')
    # Actually: replace [idx_start:idx_end] with new_content_block + "    </div>" (one closing for content-card). So we're removing the old session content which had many </div> and ended with two </div> (inner + content-card). So we need to add back "    </div>" once to close the content-card.
    new_full = before + new_content_block + "\n    </div>\n" + after
    with open(LP, "w", encoding="utf-8") as f:
        f.write(new_full)
    print("Replaced session plans with 40 chapters. OK.")

if __name__ == "__main__":
    main()
