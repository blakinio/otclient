OterynLoginTheme = OterynLoginTheme or {}

local prepared = false
local enterGameWindow
local originalIdentityUpdateUi
local originalCharacterListCreate
local originalCharacterListRebuild

local OTERYN_WIDGET_IDS = {
    'welcomeLabel',
    'welcomeDescription',
    'recommendedLabel',
    'recommendedLineLeft',
    'recommendedLineRight',
    'oterynLoginHint',
    'legacyDividerLabel',
    'legacyDividerLeft',
    'legacyDividerRight',
    'legacyModeHint'
}

local LEGACY_WIDGET_IDS = {
    'emailLabel',
    'passwordLabel',
    'legacyLoginButton'
}

local function getEnterGameWindow()
    if not enterGameWindow then
        enterGameWindow = rootWidget:recursiveGetChildById('enterGame')
    end
    return enterGameWindow
end

local function getWidget(id)
    local window = getEnterGameWindow()
    return window and window:getChildById(id) or nil
end

local function setWidgetVisible(id, visible)
    local widget = getWidget(id)
    if widget then
        widget:setVisible(visible)
    end
end

local function currentServerSupportsOteryn()
    local window = getEnterGameWindow()
    if not window or not Services or type(Services.oterynIdentity) ~= 'table' or
        Services.oterynIdentity.enabled ~= true or not Servers_init then
        return false
    end

    local hostWidget = window:getChildById('serverHostTextEdit')
    if not hostWidget then
        return false
    end

    local server = Servers_init[hostWidget:getText()]
    return OterynIdentityCore and OterynIdentityCore.serverSupportsOteryn(server) or false
end

local function stylePrimaryButton()
    local button = getWidget('oterynLoginButton')
    if not button then
        return
    end

    button:setHeight(48)
    button:setMarginLeft(386)
    button:setMarginRight(66)
    button:setMarginBottom(338)
    button:setImageSource('')
    button:setBackgroundColor('#1768d3')
    button:setBorderWidth(1)
    button:setBorderColor('#4b9cf2')
    button:setColor('#ffffff')
    button:setFont('Verdana Bold-11px')
    button:setTextOffset({ x = 0, y = 0 })
end

local function restoreConditionalLegacyWidgets()
    local rememberTip = getWidget('rememberEmailTip')
    local rememberBox = getWidget('rememberEmailBox')
    if rememberTip and rememberBox then
        rememberTip:setVisible(rememberBox:isChecked())
    end

    local forgot = getWidget('Forgot_password_email')
    if forgot then
        forgot:setVisible(Services and Services.websites and Services.websites ~= '')
    end

    local createAccount = getWidget('btnCreateNewAccount')
    if createAccount then
        local configured = Services and Servers_init and table.size(Servers_init) == 1 and Services.createAccount
        createAccount:setVisible(configured and true or false)
    end

    local stayLogged = getWidget('stayLoggedBox')
    local window = getEnterGameWindow()
    if stayLogged and window then
        stayLogged:setVisible(window.stayLoggedBoxEnabled == true)
    end
end

local function applyModeCopy()
    local legacyDivider = getWidget('legacyDividerLabel')
    if legacyDivider then
        legacyDivider:setText(tr('LEGACY SERVER MODE'))
    end

    local legacyHint = getWidget('legacyModeHint')
    if legacyHint then
        legacyHint:setText(tr('Account and password login remains available on separate compatible custom-server profiles.'))
    end

    local loginHint = getWidget('oterynLoginHint')
    if loginHint then
        loginHint:setMarginTop(104)
    end

    local status = getWidget('systemsStatusLabel')
    if status then
        status:setText(tr('●  Client ready'))
    end
end

local function applyModePresentation()
    local oterynMode = currentServerSupportsOteryn()

    setWidgetVisible('oterynPanel', oterynMode)
    setWidgetVisible('legacyPanel', not oterynMode)

    for _, id in ipairs(OTERYN_WIDGET_IDS) do
        setWidgetVisible(id, oterynMode)
    end
    for _, id in ipairs(LEGACY_WIDGET_IDS) do
        setWidgetVisible(id, not oterynMode)
    end

    local createAccount = getWidget('btnCreateNewAccount')
    local forgot = getWidget('Forgot_password_email')
    local rememberTip = getWidget('rememberEmailTip')
    local stayLogged = getWidget('stayLoggedBox')

    if oterynMode then
        if createAccount then createAccount:hide() end
        if forgot then forgot:hide() end
        if rememberTip then rememberTip:hide() end
        if stayLogged then stayLogged:hide() end
    else
        restoreConditionalLegacyWidgets()
    end

    applyModeCopy()
    stylePrimaryButton()
end

local function applyOterynCharacterWindow()
    if not G.oterynGameSession then
        return nil
    end

    local window = rootWidget:recursiveGetChildById('charactersWindow')
    if not window then
        return nil
    end

    local backButton = window:getChildById('buttonCancel')
    if backButton then
        backButton:setText(tr('Back'))
    end

    local accountIcon = window:getChildById('accountStatusIcon')
    if accountIcon then
        accountIcon:setImageSource('')
    end

    return window
end

local function applyOterynCharacterRows()
    local window = applyOterynCharacterWindow()
    local list = window and window:getChildById('characters') or nil
    if not list then
        return
    end

    for index, child in ipairs(list:getChildren()) do
        local rowColor = index % 2 == 0 and '#111c28' or '#162331'
        child.rowColor = rowColor
        if not child:isFocused() then
            child:setBackgroundColor(rowColor)
        end
    end
end

function OterynLoginTheme.prepare()
    if prepared then
        return
    end
    prepared = true

    originalIdentityUpdateUi = OterynIdentity.updateUi
    OterynIdentity.updateUi = function(...)
        if originalIdentityUpdateUi then
            originalIdentityUpdateUi(...)
        end
        applyModePresentation()
    end

    originalCharacterListCreate = CharacterList.create
    CharacterList.create = function(characters, account, otui)
        if account and account.oterynIdentity and not otui then
            otui = 'oteryn_characterlist'
        end
        local result = originalCharacterListCreate(characters, account, otui)
        applyOterynCharacterRows()
        return result
    end

    originalCharacterListRebuild = CharacterList.rebuildCharactersList
    CharacterList.rebuildCharactersList = function(...)
        local result = originalCharacterListRebuild(...)
        applyOterynCharacterRows()
        return result
    end
end

function OterynLoginTheme.init()
    enterGameWindow = rootWidget:recursiveGetChildById('enterGame')
    applyModePresentation()
end

function OterynLoginTheme.terminate()
    if originalIdentityUpdateUi and OterynIdentity then
        OterynIdentity.updateUi = originalIdentityUpdateUi
    end
    if originalCharacterListCreate and CharacterList then
        CharacterList.create = originalCharacterListCreate
    end
    if originalCharacterListRebuild and CharacterList then
        CharacterList.rebuildCharactersList = originalCharacterListRebuild
    end

    originalIdentityUpdateUi = nil
    originalCharacterListCreate = nil
    originalCharacterListRebuild = nil
    enterGameWindow = nil
    prepared = false
end

return OterynLoginTheme
