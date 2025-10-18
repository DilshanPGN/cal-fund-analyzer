/**
 * Modal Component
 * Manages modal dialogs with clean encapsulation
 * Implements the Component Pattern
 */

class ModalComponent {
    /**
     * Initialize Modal Component
     * @param {HTMLElement} modalElement - Modal DOM element
     * @param {Object} config - Configuration object
     */
    constructor(modalElement, config) {
        this.modal = modalElement;
        this.config = config.ui;
        this.isOpen = false;
        this._setupEventListeners();
    }

    /**
     * Set up event listeners
     * @private
     */
    _setupEventListeners() {
        // Close on backdrop click
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
            }
        });

        // Close button
        const closeBtn = this.modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.close());
        }
    }

    /**
     * Open modal with content
     * @param {string} title - Modal title
     * @param {string|HTMLElement} content - Modal content
     */
    open(title, content) {
        const titleElement = this.modal.querySelector('#modalTitle');
        const bodyElement = this.modal.querySelector('#modalBody');

        if (titleElement) {
            titleElement.textContent = title;
        }

        if (bodyElement) {
            if (typeof content === 'string') {
                bodyElement.innerHTML = content;
            } else {
                bodyElement.innerHTML = '';
                bodyElement.appendChild(content);
            }
        }

        this.modal.style.display = 'flex';
        this.isOpen = true;

        // Animate in
        setTimeout(() => {
            this.modal.classList.add('modal-open');
        }, 10);

        // Prevent body scroll
        document.body.style.overflow = 'hidden';
    }

    /**
     * Close modal
     */
    close() {
        this.modal.classList.remove('modal-open');
        
        setTimeout(() => {
            this.modal.style.display = 'none';
            this.isOpen = false;
            
            // Restore body scroll
            document.body.style.overflow = '';
        }, this.config.modalAnimationDuration);
    }

    /**
     * Show loading state in modal
     * @param {string} message - Loading message
     */
    showLoading(message = 'Loading...') {
        const loadingHTML = `
            <div class="modal-loading">
                <div class="spinner"></div>
                <p>${message}</p>
            </div>
        `;
        this.open('Please Wait', loadingHTML);
    }

    /**
     * Show error message
     * @param {string} title - Error title
     * @param {string} message - Error message
     */
    showError(title, message) {
        const errorHTML = `
            <div class="modal-error">
                <div class="error-icon">❌</div>
                <p>${message}</p>
            </div>
        `;
        this.open(title, errorHTML);
    }

    /**
     * Show success message
     * @param {string} title - Success title
     * @param {string} message - Success message
     */
    showSuccess(title, message) {
        const successHTML = `
            <div class="modal-success">
                <div class="success-icon">✅</div>
                <p>${message}</p>
            </div>
        `;
        this.open(title, successHTML);
    }

    /**
     * Show confirmation dialog
     * @param {string} title - Dialog title
     * @param {string} message - Dialog message
     * @param {Function} onConfirm - Callback on confirm
     * @param {Function} onCancel - Callback on cancel
     */
    showConfirmation(title, message, onConfirm, onCancel = null) {
        const confirmHTML = `
            <div class="modal-confirm">
                <p>${message}</p>
                <div class="modal-actions">
                    <button class="btn btn-primary modal-confirm-yes">Yes</button>
                    <button class="btn btn-secondary modal-confirm-no">No</button>
                </div>
            </div>
        `;
        
        this.open(title, confirmHTML);

        // Add event listeners to buttons
        const yesBtn = this.modal.querySelector('.modal-confirm-yes');
        const noBtn = this.modal.querySelector('.modal-confirm-no');

        yesBtn.addEventListener('click', () => {
            this.close();
            if (onConfirm) onConfirm();
        });

        noBtn.addEventListener('click', () => {
            this.close();
            if (onCancel) onCancel();
        });
    }

    /**
     * Check if modal is currently open
     * @returns {boolean}
     */
    isModalOpen() {
        return this.isOpen;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ModalComponent;
}

