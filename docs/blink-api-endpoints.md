# Blink Android app 60.0 — full REST endpoint list

Extracted from the decompiled app's Retrofit interfaces (323 annotations). `%7Binjected_account_id%7D` / `%7Binjected_client_id%7D` are filled in by the app at request time with your account_id / client_id.

323 unique endpoints across 60 API interfaces.

## AccessApi

| Method | Path | App function | Params |
|---|---|---|---|
| PATCH | `v1/shared/authorizations/{authorizationId}` | patchFriendlyName | Path:authorizationId, Query:first_request, Body:FriendlyNamePatchBody |
| DELETE | `v1/shared/authorizations/{authorizationId}/remove` | deleteRemoveAccess | Path:authorizationId |
| DELETE | `v1/shared/authorizations/{authorizationId}/revoke` | deleteRevokeAccess | Path:authorizationId |
| GET | `v1/shared/check_authorization` | getCheckAuthorization | Query:friendly_name |
| POST | `v1/shared/invitations/send` | postSendInvite | Body:SendInviteBody |
| POST | `v1/shared/invitations/{invitationId}/accept` | postAcceptAccess | Path:invitationId, Body:AcceptInvitationBody |
| DELETE | `v1/shared/invitations/{invitationId}/decline` | deleteDeclineInvite | Path:invitationId |
| DELETE | `v1/shared/invitations/{invitationId}/revoke` | deleteRevokeInvite | Path:invitationId |
| PATCH | `v1/shared/popovers/{popoverId}/read` | popoverRead | Path:popoverId |
| GET | `v1/shared/summary` | getSharedSummary |  |

## AccessoryApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/accessories/delete` | delete | Path:network_id, Body:DeleteAccessoryBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/accessories/add` | addAccessory | Body:AddAccessoryBody, Path:network |

## AccountApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `/users/delete` | deleteAccount | Body:DeleteAccountBody |
| POST | `v1/countries/update` | setAccountCountry | Body:CountryBody |
| POST | `v1/identity/token` | postTokenUpgrade | Body:TokenUpgradePostBody |
| GET | `v1/notifications/preferences` | getNotificationPreferences |  |
| POST | `v1/notifications/preferences` | postNotificationPreferences | Body:NotificationPreferencesResponse |
| POST | `v1/users/authenticate_password` | authenticatePassword | Body:AuthenticatePasswordBody |
| POST | `v1/users/countries/update` | updateUserCountry | Body:CountryBody |
| GET | `v1/users/options` | getAccountOptions |  |
| GET | `v1/users/preferences` | getAccountPreferences |  |
| POST | `v1/users/preferences` | postAccountPreferences | Body:AccountPreferencesBody |
| GET | `v1/users/tier_info` | getTierInfo |  |
| GET | `v2/users/info` | getAccountInfo |  |
| POST | `v4/clients/%7Binjected_client_id%7D/logout` | logout |  |
| POST | `v4/users/pin/resend` | postRegistrationPinResend |  |
| POST | `v4/users/pin/verify` | postRegistrationPinVerify | Body:VerifyPinPostBody |

## AlexaLinkingApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v1/alexa/authorization` | postAuthorization | Body:AlexaLinkingAuthorizePostBody |
| DELETE | `v1/alexa/link` | deleteLink |  |
| POST | `v1/alexa/link` | postLink | Body:AlexaLinkingLinkPostBody |
| GET | `v1/alexa/link_status` | getLinkStatus |  |

## AuthApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v3/users/validate_email` | postValidateEmail | Body:ValidateEmailPostBody |
| POST | `v3/users/validate_password` | postValidatePassword | Body:ValidatePasswordPostBody |
| POST | `v7/users/register` | postRegister | Body:RegisterBody |

## BlinkCloudLocationApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v1/locations/update` | notifyLocationUpdate |  |

## CameraApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `/accounts/%7Binjected_account_id%7D/networks/{networkId}/cameras/{cameraId}/delete` | deleteCamera | Path:networkId, Path:cameraId |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{networkId}/cameras/{cameraId}/status` | postCameraStatusCommand | Path:networkId, Path:cameraId |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/add` | addCamera | Body:AddCameraBody, Path:network |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/thumbnail` | postThumbnail | Path:network, Path:camera |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/{type}` | postCameraMotion | Path:network, Path:camera, Path:type |
| POST | `/api/v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/cameras/{camera}/lights/{lightControl}` | postIntegratedLight | Path:networkId, Path:camera, Path:lightControl |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/cameras/{cameraId}/network_type` | getVideoNetworkType | Path:networkId, Path:cameraId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/cameras/{cameraId}/network_type` | postVideoNetworkType | Path:networkId, Path:cameraId, Body:VideoNetworkTypeBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/cameras/{camera}/accessories/{accessoryType}/{accessoryId}/delete` | deleteAccessory | Path:networkId, Path:camera, Path:accessoryType, Path:accessoryId |
| DELETE | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{primary_id}/pair` | deleteCameraPair | Path:networkId, Path:primary_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{primary_id}/pair` | postPairCameras | Path:networkId, Path:primary_id, Body:PairCameraBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{primary_id}/swap_pair` | postSwapPair | Path:networkId, Path:primary_id, Body:SwapCameraBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/cameras/{camera_id}/snooze` | snoozeCamera | Path:network_id, Path:camera_id, Body:SnoozeBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/cameras/{camera_id}/unsnooze` | unSnoozeCamera | Path:network_id, Path:camera_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/calibrate` | saveCalibrateTemperature | Body:TemperatureCalibrationPostBody, Path:network, Path:camera |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/programs` | getCameraPrograms | Path:network, Path:camera |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/programs/create` | createCameraProgram | Body:CreateProgramBody, Path:network, Path:camera |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/programs/{program}/delete` | deleteCameraProgram | Path:network, Path:camera, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/programs/{program}/disable` | disableCameraProgram | Path:network, Path:camera, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/programs/{program}/enable` | enableCameraProgram | Path:network, Path:camera, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/programs/{program}/update` | updateCameraProgram | Body:CreateProgramBody, Path:network, Path:camera, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/temp_alert_disable` | tempAlertDisable | Path:network, Path:camera |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/temp_alert_enable` | tempAlertEnable | Path:network, Path:camera |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/zones` | getZones | Path:network, Path:camera |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/zones` | setZones | Body:AdvancedCameraZones, Path:network, Path:camera |
| POST | `v2/accounts/%7Binjected_account_id%7D/networks/{networkId}/cameras/{cameraId}/config` | postCameraConfig | Body:UpdateCameraBody, Path:networkId, Path:cameraId |
| POST | `v2/accounts/%7Binjected_account_id%7D/networks/{networkId}/cameras/{camera}/light_accessories/{accessoryId}/lights/{lightControl}` | postAccessoryLight | Path:networkId, Path:camera, Path:accessoryId, Path:lightControl |
| GET | `v2/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/config` | getCameraConfig | Path:network, Path:camera |
| GET | `v2/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/zones` | getZonesV2 | Path:network, Path:camera |
| POST | `v2/accounts/%7Binjected_account_id%7D/networks/{network}/cameras/{camera}/zones` | setZonesV2 | Body:ZoneV2Response, Path:network, Path:camera |
| POST | `v6/accounts/%7Binjected_account_id%7D/networks/{networkId}/cameras/{cameraId}/liveview` | postLiveViewCommand | Path:networkId, Path:cameraId, Body:LiveViewCommandPostBody |

## ClientApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `/clients/%7Binjected_client_id%7D/update` | postClientUpdate | Body:ClientUpdatePostBody |
| GET | `v1/clients/%7Binjected_client_id%7D/options` | getClientOptions |  |
| POST | `v1/clients/%7Binjected_client_id%7D/options` | postClientOptions | Body:ClientOptionsBody |
| POST | `v4/clients/%7Binjected_client_id%7D/pin/verify` | verifyClientPIN | Body:VerifyPinBody |
| POST | `v5/clients/%7Binjected_client_id%7D/client_verification/pin/resend` | resendClientVerificationCode |  |
| POST | `v5/clients/%7Binjected_client_id%7D/client_verification/pin/verify` | submitClientVerificationCode | Body:SubmitVerificationRequest |

## ClientDeviceManagementApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v1/clients/%7Binjected_client_id%7D/control_panel/clients` | getClients |  |
| POST | `v1/clients/%7Binjected_client_id%7D/control_panel/delete` | deleteClient | Body:DeleteClientBody |
| POST | `v1/clients/%7Binjected_client_id%7D/control_panel/pin/resend` | postManageClientsPinResend |  |
| POST | `v1/clients/%7Binjected_client_id%7D/control_panel/pin/verify` | postManageClientsPinVerify | Body:VerifyPinPostBody |
| POST | `v1/clients/%7Binjected_client_id%7D/control_panel/request_pin` | postManageClientsPinGenerate |  |

## ClientsApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `factory_profile` | startSetupV1 | Body:CreateSetupBodyV1 |
| POST | `setups` | startSetupV1 | Body:CreateSetupBodyV1 |
| POST | `setups` | startSetupV2 | Body:CreateSetupBodyV2 |
| GET | `setups/{setupId}` | startSetupV1 | Body:CreateSetupBodyV1 |
| POST | `setups/{setupId}/complete` | startSetupV1 | Body:CreateSetupBodyV1 |

## CommandApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `/accounts/%7Binjected_account_id%7D/networks/{network}/commands/{command}` | commandPoll | Path:network, Path:command |
| GET | `/accounts/%7Binjected_account_id%7D/networks/{network}/commands/{command}` | commandPollCameraAction | Path:network, Path:command |
| GET | `/accounts/%7Binjected_account_id%7D/networks/{network}/commands/{command}` | commandPollLiveView | Path:network, Path:command |
| GET | `/accounts/%7Binjected_account_id%7D/networks/{network}/commands/{command}` | commandPollWithChildren | Path:network, Path:command |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/commands/{command}/done` | terminateOnboardingCommand | Body:TerminateOnboardingBody, Path:network, Path:command |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/commands/{command}/update` | postUpdateCommand | Body:UpdateCommandRequest, Path:network, Path:command |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/commands/{command}/update` | terminateOnboardingCommand | Body:TerminateOnboardingBody, Path:network, Path:command |

## CommandsApi

| Method | Path | App function | Params |
|---|---|---|---|
| PATCH | `devices/{deviceId}` | patchDeviceCommand | Path:deviceId, Body:RequestBody |

## CustomerSupportAccessApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v2/clients/%7Binjected_client_id%7D/tiv` | postTivLock | Body:TivLockBody |
| POST | `v2/clients/%7Binjected_client_id%7D/tiv_unlock/pin/resend` | postTivUnlockPinResend |  |
| POST | `v2/clients/%7Binjected_client_id%7D/tiv_unlock/pin/verify` | postTivUnlockPinVerify | Body:VerifyPinPostBody |
| POST | `v2/clients/%7Binjected_client_id%7D/tiv_unlock/request_pin` | postTivUnlockPinGenerate |  |

## DeviceApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v1/accounts/%7Binjected_account_id%7D/devices/{serial}/token` | getDeviceAuthToken | Path:serial |
| GET | `v2/accounts/%7Binjected_account_id%7D/devices/identify/{serialNumber}` | getDeviceIdentity | Path:serialNumber |

## DeviceRegistryApi

| Method | Path | App function | Params |
|---|---|---|---|
| PATCH | `devices/v1/devices/{deviceId}` | patchDevice | Path:deviceId, Body:DeviceRegistryPatchBody, Query:ignore_rbac |
| PATCH | `devices/v1/devices/{deviceId}/settings` | patchDeviceFirmwareSettings | Path:deviceId, Body:DeviceFirmwareSettingsPatchBody |

## DeviceUpdateOrchestrationServiceApi

| Method | Path | App function | Params |
|---|---|---|---|
| PUT | `duos/v1/devices/update` | updateDevices | Body:DeviceBulkUpdateRequest |
| PATCH | `duos/v1/devices/{deviceId}/component_settings/motion` | patchZoneSettings | Path:deviceId, Query:zone_type, Body:DuosZoneSettingsRequest |
| PUT | `duos/v1/devices/{deviceId}/update` | putZoneMask | Path:deviceId, Body:DuosZoneMaskRequest |
| PUT | `duos/v1/devices/{deviceId}/update` | requestSnapshot | Path:deviceId, Body:DuosSnapshotRequest |
| PUT | `duos/v1/devices/{deviceId}/update` | updateAudioSettings | Path:deviceId, Body:DeviceAudioSettingsUpdateRequest |
| PUT | `duos/v1/devices/{deviceId}/update` | updateDevice | Path:deviceId, Body:DeviceEntityUpdateRequest |
| PUT | `duos/v1/devices/{deviceId}/update` | updateMotionSettings | Path:deviceId, Body:DeviceMotionSettingsUpdateRequest |
| PUT | `duos/v1/devices/{deviceId}/update` | updatePrivacySettings | Path:deviceId, Body:DevicePrivacySettingsUpdateRequest |
| PUT | `duos/v1/devices/{deviceId}/update` | updateVideoPhotoSettings | Path:deviceId, Body:DeviceVideoPhotoSettingsUpdateRequest |

## DoorbellApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v1/accounts/%7Binjected_account_id%7D/doorbells/{serial}/fw_update` | downloadLotusFirmwareUpdate | Path:serial |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/doorbells/ob_cancel` | postDoorbellOnboardingCancel | Body:CancelOnboardingPostBody, Path:networkId |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/doorbells/{doorbellId}/owl_as_chime/list` | getChimeCameras | Path:networkId, Path:doorbellId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/doorbells/{doorbellId}/owl_as_chime/update` | postChimeCameras | Path:networkId, Path:doorbellId, Body:ChimeCamerasPostBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/doorbells/{lotusId}/config` | postDoorbellConfig | Body:UpdateLotusBody, Path:networkId, Path:lotusId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/doorbells/{lotusId}/delete` | deleteDoorbell | Path:networkId, Path:lotusId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/doorbells/{lotusId}/status` | postDoorbellStatusCommand | Path:networkId, Path:lotusId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/doorbells/{doorbell_id}/change_mode` | lotusChangeMode | Path:network_id, Path:doorbell_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/doorbells/{doorbell_id}/change_wifi` | changeLotusWifi | Body:OnboardingBody, Path:network_id, Path:doorbell_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/doorbells/{doorbell_id}/clear_creds` | lotusClearCreds | Path:network_id, Path:doorbell_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/doorbells/{doorbell_id}/stay_awake` | keepLotusAwake | Path:network_id, Path:doorbell_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/doorbells/{lotus_id}/snooze` | snoozeLotus | Path:network_id, Path:lotus_id, Body:SnoozeBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/doorbells/{lotus_id}/unsnooze` | unSnoozeLotus | Path:network_id, Path:lotus_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/add` | addLotus | Body:AddLotusBody, Path:network |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{doorbellId}/calibrate` | postTemperatureCalibration | Body:TemperatureCalibrationPostBody, Path:network, Path:doorbellId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{doorbellId}/temp_alert_disable` | postTempAlertDisable | Path:network, Path:doorbellId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{doorbellId}/temp_alert_enable` | postTempAlertEnable | Path:network, Path:doorbellId |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{doorbell}/chime/{chimeType}/config` | getLotusChimeConfig | Path:chimeType, Path:network, Path:doorbell |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{doorbell}/chime/{chimeType}/config` | setLotusChimeConfig | Path:chimeType, Path:network, Path:doorbell, Body:UpdateLotusChimeConfig |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{doorbell}/config` | getDoorbellConfig | Path:network, Path:doorbell |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{doorbell}/power_test` | performLotusPowerAnalysis | Path:network, Path:doorbell |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{doorbell}/trigger_chime` | testLotusDing | Path:network, Path:doorbell, Body:TestLotusDingConfig |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{lotus}/disable` | postDisableLotus | Path:network, Path:lotus |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{lotus}/enable` | postEnableLotus | Path:network, Path:lotus |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{lotus}/status` | refreshLotusStatus | Path:network, Path:lotus |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{lotus}/status` | refreshLotusStatusSuspend | Path:network, Path:lotus |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{lotus}/thumbnail` | postThumbnail | Path:network, Path:lotus |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{lotus}/zones` | getLotusZones | Path:network, Path:lotus |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{lotus}/zones` | setLotusZones | Body:AdvancedCameraZones, Path:network, Path:lotus |
| POST | `v2/accounts/%7Binjected_account_id%7D/networks/{networkId}/doorbells/{doorbellId}/liveview` | postLiveViewCommand | Path:networkId, Path:doorbellId, Body:LiveViewCommandPostBody |
| GET | `v2/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{lotus}/zones` | getZonesV2 | Path:network, Path:lotus |
| POST | `v2/accounts/%7Binjected_account_id%7D/networks/{network}/doorbells/{lotus}/zones` | setZonesV2 | Body:ZoneV2Response, Path:network, Path:lotus |

## EmailChangeApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v4/clients/%7Binjected_client_id%7D/email_change` | postEmailChange | Body:ChangeEmailPostBody |
| POST | `v4/clients/%7Binjected_client_id%7D/email_change/pin/resend` | postEmailChangePinGenerate |  |
| POST | `v4/clients/%7Binjected_client_id%7D/email_change/pin/verify` | postEmailChangePinVerify | Body:VerifyPinPostBody |

## EventApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v1/events/app` | trackEvents | Body:TrackingEvents |

## EventAssociationsApi

| Method | Path | App function | Params |
|---|---|---|---|
| HTTP | `hasBody = false, method = "DELETE", path = "v1/history/events/associations/{profile_id}` | deleteEventAssociations | Path:profile_id, Query:filter[event_ids] |

## EventStreamApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `1.0.0/batch/client.device/{appSubGroup}` | sendBatchEvents | Header:Authorization, Path:appSubGroup, Body:RequestBody |
| POST | `1.0.0/event/client.device/{appSubGroup}` | trackEvent | Header:Authorization, Path:appSubGroup, Body:RequestBody |

## FeatureFlagApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v1/accounts/%7Binjected_account_id%7D/feature_flags/enabled` | getFeatureFlags |  |

## GeocodingApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `geocoding/v1/auto-complete` | getLocationSearch | Query:input, Query:language, Query:place-type |
| GET | `geocoding/v1/auto-complete/details` | getSuggestionDetails | Query:id, Query:language |
| POST | `geocoding/v1/geocode` | postGeoCodingDetails | Body:GeoCodingRequest |
| GET | `geocoding/v1/ip/info/my` | getLocationByIp |  |
| GET | `geocoding/v1/reverse-geocode` | getAddressFromLatLng | Query:lat, Query:lng, Query:language |

## HomeScreenApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v4/accounts/%7Binjected_account_id%7D/homescreen` | getHomeScreen |  |

## IdentitiesApi

| Method | Path | App function | Params |
|---|---|---|---|
| HTTP | `hasBody = false, method = "DELETE", path = "v1/identities/{id}/enrollment-images` | deleteEnrollmentImages | Path:id, Query:filter[id] |
| GET | `v1/identities` | getIdentities |  |
| DELETE | `v1/identities/{id}` | deleteIdentity | Path:id |
| GET | `v1/identities/{id}` | getIdentity | Path:id, Query:include |
| PATCH | `v1/identities/{id}` | updateIdentity | Path:id, Body:UpdateIdentityRequest |
| PATCH | `v1/identities/{id}/actions/merge-identities` | mergeIdentities | Path:id, Body:MergeIdentitiesRequest |
| POST | `v1/identities/{id}/actions/split-identity` | splitIdentity | Path:id, Body:SplitIdentityRequest |
| PATCH | `v1/identities/{id}/enrollment-images/actions/move-enrollment-images` | moveEnrollmentImages | Path:id, Body:MoveEnrollmentImagesRequest |

## KnownFacesRdisApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v1/devices` | getDevices | Query:include |
| PATCH | `v1/devices/{id}/configurations` | updateDeviceConfiguration | Path:id, Body:UpdateDeviceConfigurationRequest |

## LinkDeviceApi

| Method | Path | App function | Params |
|---|---|---|---|
| DELETE | `/blink/clients_api/links/v1/locations/{locationId}/devices/{deviceId}/links/{linkId}?ignore_rbac=true&include_deactivated=false` | deleteLink | Path:locationId, Path:deviceId, Path:linkId |
| GET | `/blink/clients_api/links/v1/locations/{locationId}/devices/{deviceId}/links?ignore_rbac=true&include_deactivated=false` | getDeviceLinks | Path:locationId, Path:deviceId, Query:inbound |
| POST | `/blink/clients_api/links/v1/locations/{locationId}/events/{event}/receivers?ignore_rbac=true&include_deactivated=false` | createLink | Path:locationId, Path:event, Body:CreateLinkRequest |

## LocalSetupOrchestrationServiceApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `system/config/network` | getNetworkConfig |  |
| POST | `system/config/network` | postNetworkConfig | Body:NetworkConfigPostBody |
| POST | `system/config/reg_domain` | postRegionConfig | Body:RegionConfigPostBody |
| GET | `system/prov/ap_list` | getAccessPointList |  |

## LocationSubtypeApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `location-subtypes` | getLocationSubtypes |  |

## LocationsCoreApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `devices/v2/locations` | getLocationsV1 |  |
| POST | `duos/v1/locations` | postLocation | Body:PutLocationRequest |
| POST | `duos/v1/locations` | postLocationRaw | Body:PutLocationRequest |
| DELETE | `duos/v1/locations/{locationId}` | deleteLocation | Path:locationId |
| PATCH | `duos/v1/locations/{locationId}` | patchLocation | Path:locationId, Body:UpdateLocationRequest |
| PATCH | `duos/v1/locations/{locationId}` | patchLocationRaw | Path:locationId, Body:UpdateLocationRequest |
| GET | `location_info/v3/locations` | getLocationsV3 | Query:ignore_rbac |

## LogApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `/app/logs/upload` | sendLogs | Body:LogsBody |

## ManageDataApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v1/data_request/dsar/create` | postDsarRequest |  |
| POST | `v1/data_request/euda/create` | postEudaRequest |  |
| GET | `v1/data_request/list` | getDataRequests |  |
| POST | `v1/data_request/third_party/{thirdPartyId}/revoke` | postRevoke | Path:thirdPartyId |

## MediaApi

| Method | Path | App function | Params |
|---|---|---|---|
| DELETE | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/local_storage` | getDeleteAllKommand | Path:networkId, Path:syncModuleId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/local_storage/manifest/request` | getLocalStorageManifestKommand | Path:networkId, Path:syncModuleId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/local_storage/manifest/{manifestId}/clip/delete/{clipId}` | getDeleteLocalStorageMediaKommand | Path:networkId, Path:syncModuleId, Path:clipId, Path:manifestId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/local_storage/manifest/{manifestId}/clip/request/{clipId}` | getClipKommand | Path:networkId, Path:syncModuleId, Path:clipId, Path:manifestId |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/local_storage/media/{commandId}` | getLocalStorageMedia | Path:networkId, Path:syncModuleId, Path:commandId |
| POST | `v4/accounts/%7Binjected_account_id%7D/media` | postMedia | Query:start_time, Query:end_time, Query:pagination_key, Body:MediaPostBody |
| POST | `v4/accounts/%7Binjected_account_id%7D/media/delete` | postDeleteMedia | Body:MediaListBody |
| POST | `v4/accounts/%7Binjected_account_id%7D/media/favorite` | postFavoriteMedia | Body:FavoriteEventIdsBody |
| POST | `v4/accounts/%7Binjected_account_id%7D/media/mark_as_viewed` | postMarkAsViewed | Body:MediaListBody |
| POST | `v4/accounts/%7Binjected_account_id%7D/media/unfavorite` | postUnfavoriteMedia | Body:FavoriteEventIdsBody |
| DELETE | `v4/accounts/%7Binjected_account_id%7D/media/{mediaId}/delete` | deleteCloudMedia | Path:mediaId |
| GET | `v4/accounts/%7Binjected_account_id%7D/media_settings` | getMediaSettings |  |
| PATCH | `v4/accounts/%7Binjected_account_id%7D/media_settings` | patchMediaSettings | Body:MediaSettingsPatch |
| GET | `v4/accounts/%7Binjected_account_id%7D/unwatched_media` | getUnwatchedMedia |  |

## NetworkApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `/accounts/%7Binjected_account_id%7D/networks/add` | createSystem | Body:AddNetworkBody |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/delete` | deleteSystem | Path:network |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/update` | updateNetworkSaveAllLiveViews | Body:UpdateNetworkSaveAllLiveViews, Path:network |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/update` | updateSystem | Body:UpdateSystemNameBody, Path:network |
| POST | `/accounts/%7Binjected_account_id%7D/networks/{network}/update` | updateTimezone | Body:UpdateTimezoneBody, Path:network |
| POST | `/accounts/%7Binjected_account_id%7D/system_offline/{network}` | sendSystemOfflineHelpEmail | Path:network |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/bulk_location_assignment` | bulkLocationAssignment | Body:BulkLocationAssignmentRequest |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/state/arm` | postArmNetwork | Path:networkId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/state/{type}` | armDisarmNetwork | Path:networkId, Path:type |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/snooze` | snoozeSystem | Path:network_id, Body:SnoozeBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/state/disarm` | disarmNetwork | Path:network_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/unsnooze` | unSnoozeSystem | Path:network_id |

## NotificationApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v2/notification` | acknowledgeNotification | Body:AcknowledgeNotificationBody |

## OauthApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `oauth/token` | postLogin | Field:username, Field:password, Header:2fa-code, Header:hardware_id, Field:grant_type, Field:client_id, Field:scope |

## OwlApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{camera}/accessories/{accessoryType}/{accessoryId}/delete` | deleteAccessory | Path:networkId, Path:camera, Path:accessoryType, Path:accessoryId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{camera}/lights/{lightControl}` | postLight | Path:networkId, Path:camera, Path:lightControl |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{camera}/lights/{lightControl}` | postLightOld | Path:networkId, Path:camera, Path:lightControl |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/change_wifi` | changeOwlWifi | Body:OnboardingBody, Path:networkId, Path:owlId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/change_wifi` | postChangeOwlWifi | Body:AddOwlPostBody, Path:networkId, Path:owlId |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/config` | getOwlConfig | Path:networkId, Path:owlId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/config` | postOwlConfig | Body:UpdateOwlBody, Path:networkId, Path:owlId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/config` | postOwlConfigCommand | Body:UpdateOwlBody, Path:networkId, Path:owlId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/delete` | deleteOwl | Path:networkId, Path:owlId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/status` | postOwlStatusCommand | Path:networkId, Path:owlId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/thumbnail` | postThumbnail | Path:networkId, Path:owlId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/accessories/rosie/owl/{owl_id}/calibrate` | calibrateRosie | Path:network_id, Path:owl_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/owls/{owl_id}/accessories/rosie/{rosie_id}/delete` | deleteRosie | Path:network_id, Path:owl_id, Path:rosie_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/owls/{owl_id}/snooze` | snoozeOwl | Path:network_id, Path:owl_id, Body:SnoozeBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network_id}/owls/{owl_id}/unsnooze` | unSnoozeOwl | Path:network_id, Path:owl_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/owls/add` | postAddOwl | Body:AddOwlPostBody, Path:network |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/owls/add` | startOwlOnboardingOld | Body:OnboardingBody, Path:network |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/owls/{owl}/programs` | getOwlPrograms | Path:network, Path:owl |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/owls/{owl}/programs/create` | createOwlProgram | Body:CreateProgramBody, Path:network, Path:owl |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/owls/{owl}/programs/{program}/delete` | deleteOwlProgram | Path:network, Path:owl, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/owls/{owl}/programs/{program}/disable` | disableOwlProgram | Path:network, Path:owl, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/owls/{owl}/programs/{program}/enable` | enableOwlProgram | Path:network, Path:owl, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/owls/{owl}/programs/{program}/update` | updateOwlProgram | Body:CreateProgramBody, Path:network, Path:owl, Path:program |
| GET | `v1/accounts/%7Binjected_account_id%7D/owls/{serial}/fw_update` | downloadOwlFirmwareUpdate | Path:serial |
| POST | `v2/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/liveview` | postLiveViewCommand | Path:networkId, Path:owlId, Body:LiveViewCommandPostBody |
| GET | `v2/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/zones` | getZonesV2 | Path:networkId, Path:owlId |
| POST | `v2/accounts/%7Binjected_account_id%7D/networks/{networkId}/owls/{owlId}/zones` | setZonesV2 | Body:ZoneV2Response, Path:networkId, Path:owlId |

## PasskeyOauthApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `oauth/v2/verify_otp` | verifyOtp | Field:scope, Field:client_id, Field:app_brand |

## PasskeyRegistrationApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `2fa/v1/webauthn/registration` | startRegistration | Header:hardware_id, Body:RegistrationRequest |
| POST | `2fa/v1/webauthn/registration/verify` | verifyRegistration | Header:hardware_id, Body:VerifyRegistrationRequest |

## PasswordChangeApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v4/clients/%7Binjected_client_id%7D/password_change` | changePassword | Body:ResetPasswordPostBody |
| POST | `v4/clients/%7Binjected_client_id%7D/password_change` | postPasswordChange | Body:ResetPasswordPostBody |
| POST | `v4/clients/%7Binjected_client_id%7D/password_change/pin/generate` | postPasswordChangePinGenerate |  |
| POST | `v4/clients/%7Binjected_client_id%7D/password_change/pin/verify` | postPasswordChangePinVerify | Body:VerifyPinPostBody |

## PasswordResetApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v4/users/password_change` | postPasswordReset | Body:ResetPasswordPostBody |
| POST | `v4/users/password_change/pin/generate` | postPasswordResetPinGenerate | Body:GeneratePinPostBody |
| POST | `v4/users/password_change/pin/verify` | postPasswordResetPinVerify | Body:VerifyPinPostBody |

## PhoneNumberChangeApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v5/clients/%7Binjected_client_id%7D/phone_number_change` | changePhoneNumber | Body:ChangePhoneNumberBody |
| POST | `v5/clients/%7Binjected_client_id%7D/phone_number_change` | postPhoneNumberChange | Body:AddPhoneNumberPostBody |
| POST | `v5/clients/%7Binjected_client_id%7D/phone_number_change/pin/verify` | postPhoneNumberChangePinVerify | Body:SubmitVerificationRequest |

## ProgramApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/programs` | getPrograms | Path:network |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/programs/create` | createProgram | Body:Program, Path:network |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/programs/{program}/delete` | deleteProgram | Path:network, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/programs/{program}/disable` | disableProgram | Path:network, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/programs/{program}/enable` | enableProgram | Path:network, Path:program |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{network}/programs/{program}/update` | updateProgram | Body:UpdateProgramRequest, Path:network, Path:program |

## PublicApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `//apphelp.immedia-semi.com/link-manifest.json` | getLinkManifest |  |
| GET | `/regions` | getRegions |  |
| GET | `v1/countries` | getCountries |  |
| GET | `v1/version` | getAppVersionCheck |  |

## RdisApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `device_info/v4/devices` | getDevices | Query:filter[location], Query:include, Query:ignore_rbac |
| POST | `device_info/v4/devices/operations` | postOperations | Body:RdisOperationsBody, Query:ignore_rbac |
| GET | `device_info/v4/devices/{deviceId}` | getDevice | Path:deviceId, Query:include, Query:ignore_rbac |

## ReadSubscriptionApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v1/accounts/%7Binjected_account_id%7D/access` | getAccess |  |
| GET | `v2/accounts/%7Binjected_account_id%7D/subscriptions/entitlements` | getEntitlements |  |
| GET | `v4/accounts/%7Binjected_account_id%7D/subscriptions/plans` | getSubscriptionsV4 |  |

## SetupOrchestrationServiceApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `clients_api/setups` | postStartSetup | Body:SosSetupPostBody |
| GET | `clients_api/setups/{setupId}` | getSetupStatus | Path:setupId |
| GET | `device_info/v4/devices/{deviceId}` | getDeviceConfig | Path:deviceId, Query:ignore_rbac, Query:include |
| GET | `device_info/v4/devices/{deviceId}/configurations` | getDeviceInfoConfig | Path:deviceId, Query:ignore_rbac |
| GET | `device_info/v4/devices/{deviceId}/status` | getDeviceStatus | Path:deviceId, Query:ignore_rbac |
| DELETE | `devices/v1/devices/{deviceId}` | deleteDevice | Path:deviceId |
| PATCH | `devices/v1/devices/{deviceId}` | saveUpdatedConfig | Path:deviceId, Body:UpdateSosDeviceBody |
| PATCH | `devices/v1/devices/{deviceId}` | updateDeviceLocation | Path:deviceId, Body:UpdateSosDeviceLocationBody |
| GET | `sos/v1/factory_profile` | getFactoryProfile | Query:mac_id, Query:serial_number |
| POST | `sos/v1/setups` | postChimeSetup | Body:RingSosSetupPostBody |

## ShareServiceDownloadApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `share_service/v3/downloads` | downloadStatus | Body:ShareServiceDownloadRequest |
| PUT | `share_service/v3/downloads` | requestDownload | Body:ShareServiceDownloadRequest |

## SharedLoginApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v1/clients/%7Binjected_client_id%7D/shared_login/pin/resend` | postSharedLoginPinResend |  |
| POST | `v1/clients/%7Binjected_client_id%7D/shared_login/pin/verify` | postSharedLoginPinVerify | Body:VerifyPinPostBody |
| POST | `v1/clients/%7Binjected_client_id%7D/shared_login/request_pin` | postSharedLoginPinGenerate |  |
| GET | `v1/shared_login` | getSharedLogins | Query:code, Query:pagination_key |
| POST | `v1/shared_login` | postSharedLogin | Body:CreateSharedLoginBody |
| POST | `v1/shared_login/revoke` | postRevokeSharedLogin | Body:RevokeSharedLoginBody |

## SharedLoginPublicApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v1/shared_login/claim` | postSharedLoginClaim | Body:SharedLoginClaimBody |
| POST | `v1/shared_login/verify` | postSharedLoginVerify | Body:SharedLoginVerifyBody |

## SingleEventAlertsApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v1/accounts/%7Binjected_account_id%7D/single_event_alerts` | getSingleEventAlerts | Query:ring_location_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/single_event_alerts` | postUpdateSingleEventAlerts | Body:SingleEventAlertsPostBody |

## SmartVideoDescriptionsApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `v1/accounts/%7Binjected_account_id%7D/smart_video_descriptions` | getSmartVideoDescriptions | Query:ring_location_id |
| POST | `v1/accounts/%7Binjected_account_id%7D/smart_video_descriptions` | postUpdateSmartVideoDescriptions | Body:SmartVideoDescriptionsPostBody |
| POST | `v1/accounts/%7Binjected_account_id%7D/smart_video_descriptions/summarize` | postSummarize | Body:SummarizeClipsRequest |

## SnapshotServiceApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `blink/snapshots/next/{doorbotId}` | triggerSnapshot | Path:doorbotId, Query:extras, Query:after-ms, Query:max-wait-ms |

## SyncModuleApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/delete` | deleteSyncModule | Path:networkId, Path:syncModuleId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/local_storage/eject` | ejectUsbStorage | Path:networkId, Path:syncModuleId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/local_storage/format` | formatUsbStorage | Path:networkId, Path:syncModuleId |
| POST | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/local_storage/mount` | mountUsb | Path:networkId, Path:syncModuleId |
| GET | `v1/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{syncModuleId}/local_storage/status` | getLocalStorageStatus | Path:networkId, Path:syncModuleId |
| GET | `v1/accounts/%7Binjected_account_id%7D/sync_modules/{serial}/fw_update` | downloadFirmwareUpdate | Path:serial |
| POST | `v2/accounts/%7Binjected_account_id%7D/networks/{networkId}/sync_modules/{type}` | startSyncModuleOnboarding | Body:OnboardingBody, Path:networkId, Path:type |

## SyncModuleService

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `/api/get_fw_version` | getFirmwareVersion |  |
| POST | `/api/set/app_fw_update` | setFirmwareUpdate | Header:Content-Type, Header:X-Blink-FW-Signature, Header:Content-Length, Body:RequestBody |
| POST | `/api/set/key` | setKey | Body:RequestBody |
| POST | `/api/set/ssid` | setSSid | Body:SetSSIDBody |
| GET | `/api/version` | getVersion |  |
| GET | `api/logs` | getLogs |  |
| GET | `api/ssids` | getSsids |  |

## SystemLocationApi

| Method | Path | App function | Params |
|---|---|---|---|
| PATCH | `v1/features/system_location_assignment` | assignLocation | Body:AssignLocationPayload> |
| PATCH | `v1/features/system_location_confirmation` | confirmLocation | Body:ConfirmLocationPayload> |

## VideoDonationApi

| Method | Path | App function | Params |
|---|---|---|---|
| PUT | `share_service/v3/batch_shares` | submitBatchDonation | Body:BatchDonationRequest |

## WifiApi

| Method | Path | App function | Params |
|---|---|---|---|
| GET | `api/get_fw_version` | getFwVersion |  |
| POST | `api/set/key` | sendEncryptionKey | Body:RequestBody |

## WifiSecureApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `api/set/ssid` | setSsid | Body:SetSSIDBody |
| GET | `api/ssids` | getSsids |  |

## WriteSubscriptionApi

| Method | Path | App function | Params |
|---|---|---|---|
| POST | `v1/subscriptions/clear_popup/{type}` | postClearTrialPopup | Path:type |
| POST | `v1/subscriptions/link/link_account` | linkAmazonAccount | Body:MapLinkBody |
| POST | `v1/subscriptions/link/unlink_account` | unlinkAmazonAccount | Body:VerifyLinkAccountBody |
| DELETE | `v1/subscriptions/plans/cancel_trial` | cancelTrial |  |
| GET | `v1/subscriptions/plans/get_device_attach_eligibility` | getDeviceEligibility |  |
| POST | `v1/subscriptions/plans/renew_trial` | renewTrial |  |
| POST | `v1/subscriptions/plans/{subscriptionId}/attach` | attachPlan | Path:subscriptionId, Body:AttachPlanBody |
| POST | `v1/subscriptions/request/status/{uuid}` | subscriptionRequestStatus | Body:SubscriptionRequestStatusBody, Path:uuid |
| POST | `v2/subscriptions/plans/create_trial` | createTrial | Body:AdditionalTrialBody |
