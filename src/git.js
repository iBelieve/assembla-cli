import {spawnSync} from 'child_process'

export class Repository {
    constructor(path) {
        this.path = path || process.cwd()

        this.originUrl = this.run('ls-remote --get-url origin')

        if (this.originUrl === 'origin')
            this.originUrl = null

        this.branches = this.run('branch')
            .split('\n')
            .map(branch => branch.slice(2))

        this.mainBranch = this.hasBranch('develop') ? 'develop' : 'master'
        this.currentBranch = this.run('rev-parse --abbrev-ref HEAD')
    }

    get hasUnstagedChanges() {
        return spawnSync('git diff-index --quiet HEAD', { cwd: this.path, shell: true }).status !== 0
    }

    hasBranch(branch) {
        return this.branches.includes(branch)
    }

    run(command) {
        return spawnSync(`git ${command}`, { cwd: this.path, shell: true }).stdout.trim()
    }
}
