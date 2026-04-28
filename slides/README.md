# AI-Assisted Development Training Slides

Interactive reveal.js presentation for the AI-Assisted Development training course.

## Quick Start

### View in Browser

1. Install dependencies:
   ```bash
   npm install
   ```

2. Serve the slides locally:
   ```bash
   npx http-server
   ```

3. Open your browser to `http://localhost:8080` (or the URL shown in your terminal)

### Navigate the Slides

- **Arrow keys** (↑/↓/←/→) - Move between slides
- **ESC** - View slide overview
- **F** - Fullscreen mode
- **S** - Speaker notes (if available)
- **Space** - Next slide (linear progression)

## Slide Content

The presentation covers:

1. **Introduction** - Course goals and overview
2. **Understanding Context** - Why context matters for AI
3. **CLAUDE.md Files** - How to write project briefings
4. **Config Files** - Claude Code configuration and hooks
5. **Prompt Engineering** - Techniques for better prompts
6. **Your Toolkit** - Hands-on techniques and workflows
7. **Real Features** - Planning and implementation with AI
8. **Wrap-up** - Key takeaways and next steps

## File Structure

```
slides/
├── index.html          # Main presentation file
├── css/                # Custom styling
├── assets/             # Images and diagrams
├── node_modules/       # Dependencies (after npm install)
└── package.json        # Project metadata
```

## Customization

The slides use reveal.js with custom CSS styling. To customize:

1. Edit `index.html` to modify content
2. Edit `css/` files to change styling
3. Add images or diagrams to `assets/`

## Requirements

- **Node.js** 12+ (for running http-server)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Internet connection** (for reveal.js CDN, or use local copy)

## Tips for Instructors

- Test slides in your target browser before presenting
- Use fullscreen mode (F) for better readability
- Pause on discussion questions to let participants think
- ESC view is great for jumping to a specific slide number
- Have a backup way to display slides (screenshot, PDF) in case of tech issues

## Troubleshooting

**Slides not loading?**
- Make sure you're in the correct directory
- Check that http-server is running on the right port
- Try a different browser

**Styling looks wrong?**
- Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)
- Check that CSS files are in the `css/` folder

**Dependencies missing?**
- Run `npm install` again
- Make sure Node.js is installed (`node --version`)

## Resources

- [reveal.js Documentation](https://revealjs.com/)
- [Markdown in reveal.js](https://revealjs.com/markdown/)
- [reveal.js Themes](https://revealjs.com/themes/)
