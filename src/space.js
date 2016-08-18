import {Repository} from './git'
import open from 'open'

export class AssemblaSpace extends Repository {
    constructor(path) {
        super(path)

        if (this.originUrl == null)
            throw new Error('Can\'t identify Assembla repo: no origin found')

        const match = this.originUrl.match(/^git@git\.assembla\.com:([^.]+)(\..*)?\.git$/)

        if (match == null)
            this.originUrl.match(/^https:\/\/git\.assembla\.com\/([^.]+)(\..*)?\.git$/)

        if (match != null)
            this.name = match[0]
        else
            throw new Error(`Not inside an Assembla git repo: ${this.originUrl}`)
    }

    openUrl(url) {
        open(`https://www.assembla.com/spaces/${this.name}/${url}`)
    }

    openCodeUrl(url) {
        open(`https://www.assembla.com/code/${this.name}/${url}`)
    }

    viewMergeRequests() {
        this.openUrl('git/merge_requests')
    }

    viewTickets() {
        this.openUrl('tickets')
    }

    newTicket() {
        this.openUrl('tickets/new')
    }

    makeMergeRequest() {
        if (this.mainBranch === this.currentBranch)
            throw new Error(`Currently on the ${this.mainBranch} branch, cannot open merge request.`)

        this.openCodeUrl(`git/compare/${this.mainBranch}...${this.currentBranch}`)
    }

    applyMergeRequest(urlOrBranch) {
        if (this.hasUnstagedChanges)
            throw new Error('Git index must be empty before merging a merge request')

        const match = urlOrBranch.match(/^https:\/\/www\.assembla\.com\/spaces\/(.+)\/git\/merge_requests\/(\d+)(\?.+)?$/)

        let mergeRequest
        let mergeId
        let sourceBranch
        let targetBranch
        let tempBranch

        if (match != null) {
            const spaceName = match.group(1)
            mergeId = match.group(2)

            if (spaceName !== this.name)
                throw new Error(`Unable to merge MR from a different Assembla space: ${spaceName}`)

            mergeRequest = getMergeRequest(this.name, mergeId)

            if (mergeRequest.status !== 0)
                throw new Error('This merge request has already been merged or rejected!')

            sourceBranch = mergeRequest.source_symbol
            targetBranch = mergeRequest.target_symbol
            tempBranch = `assembla-merge-${mergeId}`
        } else {
            sourceBranch = urlOrBranch
            targetBranch = this.currentBranch
            tempBranch = `assembla-merge-${sourceBranch.replace('_', '-').replace('/', '-')}`
        }

        console.log(`Fetching merge request from ${sourceBranch}`)

        this.run(`fetch ${this.originUrl} ${sourceBranch}`)
        this.run(`branch -f ${tempBranch} FETCH_HEAD`)
        this.run(`checkout ${tempBranch}`)

        console.log(`Rebasing on top of ${targetBranch}`)
        this.run(`rebase ${targetBranch}`)

        console.log(`Merging ${sourceBranch} onto ${targetBranch}`)
        this.run(`checkout ${targetBranch}`)
        this.run(`merge --ff-only ${tempBranch}`)

        if (mergeRequest != null) {
            console.log('Closing merge request')
            closeMergeRequest(this.name, mergeId)
        }
    }
}
