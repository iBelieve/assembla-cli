import open from 'open'
import prompt from 'inquirer'
import yaml from 'yaml'
import fs from 'fs'
import fetch from 'node-fetch'

const clientId = 'dKeZ3o7E8r5yo5acwqjQXA'
const clientSecret = 'd8451207e916b468c4767e444f3a4d76'
let accessToken
let refreshToken

function loadConfig() {
    const data = yaml.load('~/.config/ansible-cli')

    accessToken = data.access_token
    refreshToken = data.refresh_token
}

function saveConfig() {
    const string = yaml.stringify({ access_token: accessToken, refresh_token: refreshToken })

    fs.writeSync('~/.config/ansible-cli', string)
}

async function signIn() {
    open(`https://api.assembla.com/authorization?client_id=${clientId}&response_type=pin_code`)

    console.log('A browser will open and ask you to sign into Assembla. When done, copy the PIN code and paste it here.')

    const answer = await prompt([{ name: 'pin', message: 'PIN code: ' }])

    const data = await apiFetch(`https://${clientId}:${clientSecret}@api.assembla.com/token?grant_type=pin_code&pin_code=${[answer.pinCode]}`, { method: 'POST' })

    accessToken = data.access_token
    refreshToken = data.refresh_token
}

async function authenticate() {
    if (accessToken == null)
        await signIn()

    const data = await apiFetch(`https://${clientId}:${clientSecret}@api.assembla.com/token?client_id=${clientId}&grant_type=refresh_token&refresh_token=${refreshToken}`)

    accessToken = data.access_token

    saveConfig()
}

export async function getMergeRequest(spaceName, mergeId) {
    await authenticate()
    return await apiFetch(`/spaces/${spaceName}/space_tools/git/merge_requests/${mergeId}.json`)
}

export async function closeMergeRequest(spaceName, mergeId) {
    await authenticate()
    return await apiFetch(`/spaces/${spaceName}/space_tools/git/merge_requests/${mergeId}/ignore.json`, { method: 'PUT' })
}

async function apiFetch(url, { headers = {}, method = 'GET' } = {}) {
    if (!url.startsWith('http')) {
        url = `https://api.assembla.com/v1${url}`
        headers['Authorization'] = `Bearer ${accessToken}`
    }

    let data = await fetch(url, { headers: headers, method: method })

    try {
        data = data.json()
    } catch (error) {
        data = data.text
    }

    if (data.error != null)
        throw new Error(data.error_description || data.error)

    return data
}

loadConfig()
