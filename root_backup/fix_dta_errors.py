# Fix missing functions in DTA Pro v4.7

with open(r'C:\Users\user\OneDrive - NHS\Documents\dtahtml\dta-pro-v3.7.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Missing functions to add
missing_functions = '''
/**
 * Toggle card expand/collapse
 */
function toggleCard(element) {
  const card = element.closest('.card');
  if (card) {
    const body = card.querySelector('.card-body');
    if (body) {
      body.style.display = body.style.display === 'none' ? 'block' : 'none';
      const icon = element.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-chevron-down');
        icon.classList.toggle('fa-chevron-up');
      }
    }
  }
}

/**
 * Show modal dialog
 */
function showModal(title, content, options = {}) {
  // Create modal if not exists
  let modal = document.getElementById('dynamicModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'dynamicModal';
    modal.className = 'modal fade';
    modal.innerHTML = `
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title"></h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body"></div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }

  modal.querySelector('.modal-title').textContent = title;
  modal.querySelector('.modal-body').innerHTML = content;

  try {
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
  } catch (e) {
    // Fallback: simple alert
    alert(title + '\\n\\n' + content.replace(/<[^>]*>/g, ''));
  }
}

/**
 * Hide modal
 */
function hideModal() {
  const modal = document.getElementById('dynamicModal');
  if (modal) {
    try {
      const bsModal = bootstrap.Modal.getInstance(modal);
      if (bsModal) bsModal.hide();
    } catch (e) {}
  }
}
'''

# Check if functions already exist
if 'function toggleCard(' not in content:
    # Find a good insertion point - after the State object initialization
    target = '// Initialize State'
    if target in content:
        idx = content.find(target)
        # Find the end of State initialization block
        end_idx = content.find('};', idx) + 2
        content = content[:end_idx] + '\n' + missing_functions + content[end_idx:]
        print('Added missing functions after State initialization')
    else:
        # Alternative: insert before </script>
        idx = content.rfind('</script>')
        content = content[:idx] + missing_functions + '\n' + content[idx:]
        print('Added missing functions before </script>')
else:
    print('toggleCard already exists')

# Save the file
with open(r'C:\Users\user\OneDrive - NHS\Documents\dtahtml\dta-pro-v3.7.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done! File saved.')
