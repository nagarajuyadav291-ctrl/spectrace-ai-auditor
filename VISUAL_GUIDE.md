# 📸 Visual Guide & Screenshots

## 🎨 UI Overview

### Main Dashboard
The SpecTrace dashboard features a modern, gradient purple design with three main sections:

1. **Task Execution Panel** (Left)
   - Large textarea for task description
   - Agent type dropdown (GPT-4, GPT-3.5, Claude-3)
   - Max steps input
   - Execute button with loading state

2. **Drift Analysis Card** (Right)
   - Three metrics displayed:
     - Drift Score (numerical)
     - Trend (increasing/decreasing/stable with color coding)
     - Average Risk (numerical)

3. **Execution History Table** (Bottom)
   - Columns: ID, Task, Risk Score, Deception, Violations, Status, Time, Actions
   - Color-coded risk badges
   - View button for each execution

## 🖼️ Component Descriptions

### Header Section
```
┌─────────────────────────────────────────────┐
│         🔍 SpecTrace                        │
│    Autonomous AI Behavior Auditor           │
└─────────────────────────────────────────────┘
```
- Large title with magnifying glass emoji
- Subtitle describing the system
- White text on gradient purple background

### Task Execution Panel
```
┌─────────────────────────────────────────────┐
│ Execute Agent Task                          │
├─────────────────────────────────────────────┤
│ Task Description                            │
│ ┌─────────────────────────────────────────┐ │
│ │ Enter task for AI agent to execute...   │ │
│ │                                          │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Agent Type          Max Steps               │
│ ┌──────────────┐   ┌──────────────┐        │
│ │ GPT-4      ▼ │   │ 10           │        │
│ └──────────────┘   └──────────────┘        │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │     🚀 Execute & Audit                  │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Drift Analysis Card
```
┌─────────────────────────────────────────────┐
│ Behavioral Drift Analysis                   │
├─────────────────────────────────────────────┤
│ ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│ │ Drift   │  │ Trend   │  │ Avg     │     │
│ │ Score   │  │         │  │ Risk    │     │
│ │ 0.150   │  │ stable  │  │ 0.35    │     │
│ └─────────┘  └─────────┘  └─────────┘     │
└─────────────────────────────────────────────┘
```

### Execution History Table
```
┌──────────────────────────────────────────────────────────────────────┐
│ Execution History                                                    │
├────┬──────────────┬──────┬──────────┬──────────┬────────┬──────────┤
│ ID │ Task         │ Risk │ Deception│ Violations│ Status │ Actions  │
├────┼──────────────┼──────┼──────────┼──────────┼────────┼──────────┤
│ 1  │ Research AI..│ 0.35 │ 12.5%    │ 2        │ ✓ Done │ [View]   │
│ 2  │ Analyze data.│ 0.67 │ 45.2%    │ 5        │ ✓ Done │ [View]   │
│ 3  │ Write code...│ 0.12 │ 5.1%     │ 0        │ ✓ Done │ [View]   │
└────┴──────────────┴──────┴──────────┴──────────┴────────┴──────────┘
```

### Execution Details Modal
```
┌─────────────────────────────────────────────────────────────┐
│ Execution Details #1                                    [×] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Task                                                        │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Research the latest AI safety papers and summarize     │ │
│ │ key findings                                            │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Risk Assessment                                             │
│ ┌──────────────────────┐  ┌──────────────────────┐        │
│ │ Risk Score: 0.35     │  │ Deception: 12.5%     │        │
│ │ (Medium)             │  │                      │        │
│ └──────────────────────┘  └──────────────────────┘        │
│                                                             │
│ Spec Violations (2)                                         │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [HIGH] No Deception                                     │ │
│ │ Agent must be truthful and transparent                  │ │
│ │ Step 3                                                  │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Execution Trace (5 steps)                                   │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Step 1                                    10:30:15 AM   │ │
│ │ 💭 Thought: I need to search for papers...             │ │
│ │ ⚡ Action: Search academic databases                    │ │
│ │ 👁️ Observation: Found 50 papers                        │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │                      Close                              │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 Color Scheme

### Primary Colors
- **Purple Gradient**: `#667eea` → `#764ba2`
- **White**: `#ffffff`
- **Dark Gray**: `#1f2937`
- **Light Gray**: `#f9fafb`

### Risk Colors
- **Low Risk (Green)**: `#10b981`
- **Medium Risk (Yellow)**: `#f59e0b`
- **High Risk (Red)**: `#ef4444`

### Status Colors
- **Completed (Green)**: `#d1fae5` background, `#065f46` text
- **Pending (Yellow)**: `#fef3c7` background, `#92400e` text

### Severity Colors
- **Critical**: `#7f1d1d` (dark red)
- **High**: `#ef4444` (red)
- **Medium**: `#f59e0b` (orange)
- **Low**: `#3b82f6` (blue)

## 📱 Responsive Design

### Desktop (1400px+)
- Two-column layout for main grid
- Full table visible
- Large modal (900px width)

### Tablet (768px - 1400px)
- Single column layout
- Scrollable table
- Medium modal (90% width)

### Mobile (< 768px)
- Stacked components
- Full-width elements
- Compact modal (95% width)

## 🎭 Animations

### Fade In
- Modal background appears with fade
- Duration: 0.2s

### Slide Up
- Modal content slides up from bottom
- Duration: 0.3s

### Hover Effects
- Buttons lift up 2px on hover
- Shadow increases
- Background color darkens

## 🔤 Typography

### Font Family
- Primary: 'Inter'
- Fallback: -apple-system, BlinkMacSystemFont, 'Segoe UI'

### Font Sizes
- **Header Title**: 3rem (48px)
- **Card Title**: 1.5rem (24px)
- **Body Text**: 1rem (16px)
- **Small Text**: 0.875rem (14px)
- **Tiny Text**: 0.75rem (12px)

### Font Weights
- **Regular**: 400
- **Semibold**: 600
- **Bold**: 700

## 🎯 Interactive Elements

### Buttons
- **Primary Button**: Purple gradient, white text, rounded corners
- **Small Button**: Solid purple, white text, compact size
- **Close Button**: Gray, large X, hover effect

### Form Inputs
- **Border**: 2px solid light gray
- **Focus**: Purple border
- **Padding**: 0.75rem
- **Border Radius**: 8px

### Cards
- **Background**: White
- **Border Radius**: 16px
- **Shadow**: 0 10px 30px rgba(0,0,0,0.2)
- **Padding**: 2rem

## 📊 Data Visualization

### Risk Badges
- Circular badges with risk score
- Color-coded background
- White text
- Font weight: 600

### Trend Indicators
- Text-based (increasing/decreasing/stable)
- Color-coded:
  - Increasing: Red
  - Decreasing: Green
  - Stable: Blue

### Violation Badges
- Red background for count
- Border-left accent on violation cards
- Severity tags with color coding

## 🎬 User Flow

### 1. Landing
User sees dashboard → Three main sections visible

### 2. Task Submission
Enter task → Select agent → Set steps → Click execute

### 3. Execution
Loading state → Progress indicator → Completion alert

### 4. Results
Table updates → New row appears → Risk score visible

### 5. Details
Click View → Modal opens → Full trace displayed

### 6. Analysis
Review violations → Check deception → Examine steps

### 7. Drift Monitoring
Check drift card → See trend → Monitor changes

## 🖱️ Interaction Patterns

### Click Actions
- Execute button → Submit task
- View button → Open modal
- Close button → Close modal
- Modal background → Close modal

### Hover Effects
- Buttons → Lift and shadow
- Table rows → Highlight
- Links → Underline

### Focus States
- Inputs → Purple border
- Buttons → Outline
- Links → Outline

## 📐 Layout Grid

### Main Grid
```
┌─────────────────────────────────────┐
│           Header (full width)       │
├──────────────────┬──────────────────┤
│  Task Panel      │  Drift Card      │
│  (2fr)           │  (1fr)           │
├──────────────────┴──────────────────┤
│     Execution History (full width)  │
└─────────────────────────────────────┘
```

### Form Grid
```
┌─────────────────────────────────────┐
│  Task Description (full width)      │
├──────────────────┬──────────────────┤
│  Agent Type      │  Max Steps       │
│  (1fr)           │  (1fr)           │
├──────────────────┴──────────────────┤
│  Execute Button (full width)        │
└─────────────────────────────────────┘
```

## 🎨 Design Principles

### Clarity
- Clear labels
- Obvious actions
- Visible feedback

### Consistency
- Uniform spacing
- Consistent colors
- Standard patterns

### Accessibility
- High contrast
- Large click targets
- Keyboard navigation

### Performance
- Fast loading
- Smooth animations
- Responsive updates

---

**This visual guide helps you understand the UI without screenshots!**

The actual application looks exactly as described above with beautiful gradients, smooth animations, and professional styling.
