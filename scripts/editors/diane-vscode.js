/**
 * diane, VS Code Extension (placeholder)
 *
 * This is a starter template for a VS Code extension.
 * To develop:
 *   1. npm init
 *   2. npm install vscode
 *   3. Implement commands below
 *   4. Package with vsce
 */

const vscode = require('vscode');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

/**
 * Capture current document to diane
 */
async function captureDocument() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor');
        return;
    }

    const content = editor.document.getText();
    const config = vscode.workspace.getConfiguration('diane');
    const tags = config.get('defaultTags', []).join(',');

    try {
        let cmd = 'diane, -v';
        if (tags) {
            cmd += ` --tags ${tags}`;
        }

        const { stdout } = await execPromise(cmd, {
            input: content
        });

        vscode.window.showInformationMessage(stdout.trim());
    } catch (error) {
        vscode.window.showErrorMessage(`diane error: ${error.message}`);
    }
}

/**
 * Capture selection to diane
 */
async function captureSelection() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage('No active editor');
        return;
    }

    const selection = editor.selection;
    const content = editor.document.getText(selection);

    if (!content) {
        vscode.window.showWarningMessage('No selection');
        return;
    }

    try {
        const { stdout } = await execPromise('diane, -v', {
            input: content
        });

        vscode.window.showInformationMessage(stdout.trim());
    } catch (error) {
        vscode.window.showErrorMessage(`diane error: ${error.message}`);
    }
}

/**
 * Quick capture with input box
 */
async function quickCapture() {
    const text = await vscode.window.showInputBox({
        prompt: 'Quick capture to diane,',
        placeHolder: 'Type your thought...'
    });

    if (!text) {
        return;
    }

    try {
        const { stdout } = await execPromise('diane, -v', {
            input: text
        });

        vscode.window.showInformationMessage(stdout.trim());
    } catch (error) {
        vscode.window.showErrorMessage(`diane error: ${error.message}`);
    }
}

/**
 * Search diane records
 */
async function searchRecords() {
    const query = await vscode.window.showInputBox({
        prompt: 'Search diane, records',
        placeHolder: 'Enter search query...'
    });

    if (!query) {
        return;
    }

    try {
        const { stdout } = await execPromise(`diane, --search "${query}"`);

        // Show results in new document
        const doc = await vscode.workspace.openTextDocument({
            content: stdout,
            language: 'markdown'
        });

        await vscode.window.showTextDocument(doc);
    } catch (error) {
        vscode.window.showErrorMessage(`diane error: ${error.message}`);
    }
}

/**
 * Show statistics
 */
async function showStats() {
    try {
        const { stdout } = await execPromise('diane, --stats');

        // Show in new document
        const doc = await vscode.workspace.openTextDocument({
            content: stdout,
            language: 'plaintext'
        });

        await vscode.window.showTextDocument(doc);
    } catch (error) {
        vscode.window.showErrorMessage(`diane error: ${error.message}`);
    }
}

/**
 * Extension activation
 */
function activate(context) {
    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('diane.captureDocument', captureDocument)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('diane.captureSelection', captureSelection)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('diane.quickCapture', quickCapture)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('diane.search', searchRecords)
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('diane.stats', showStats)
    );

    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.command = 'diane.quickCapture';
    statusBarItem.text = '$(notebook) diane,';
    statusBarItem.tooltip = 'Quick capture to diane,';
    statusBarItem.show();

    context.subscriptions.push(statusBarItem);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
