pragma solidity ^0.4.0;

/**
 * The contract is a ID, and all derived 'IDs' should match the bytecode
 * of a known 'Identity' version.
*/

contract Identity {

    address private owner;
    address private override;
    uint private blocklock;
    string public encryptionPublicKey;
    string public signingPublicKey;

    /**
     * Constructor of the Smart Identity
    */
    function Identity() {
        owner = msg.sender;
        override = owner;
        blocklock = block.number - BLOCK_HEIGHT;
    }

    function register(stirng _fname, string _lname, string _faname, string _dob, string _address, string _mobile, string _mail) {
        fname = _faname;
        lname = _lname;
        dob = _dob;
        address = _address;
        mobile = _mobile;
        mail = _mail;
    }

    /**
     * The only permission worth setting; doing the reverse is pointless as a contract
     * owner can interact with the contract as an anonymous third party simply by using
     * another public key address.
     */
    modifier onlyBy(address _account) {
        if (msg.sender != _account) {
            revert();
        }
        _;
    } 

    /**
     * Check Identity is valid using modifier.
     *
     * This will also serve as protection against forks, because at the time the chain forks,
     * we can kill the registry, which will then 'invalidate' the identities that are stored
     * on the old chain.
     */
    
    modifier checkIdentity(address identity, address registry) return (bool) {
        if ( registry.isValidContract(identity) != 1 ) {
            revert();
            _;
        }
    }

    /**
     * This event is used for standard change notification messages and outputs the following:
     * - owner of the contract
     * - event status level
     * - event message body
     */
    event ChangeNotification(address indexed sender, uint status, bytes32 notificationMsg);

    /**
     * This function is used to send events.
     * Status Level Scale:
     *  1   Error: error conditions
     *  2   Warning: warning conditions
     *  3   Significant Change: Significant change to condition
     *  4   Informational: informational messages
     *  5   Verbose: debug-level messages
     */
    function sendEvent(uint _status, bytes32 _notification) internal returns(bool) {
        ChangeNotification(owner, _status, _notification);
        return true;
    }

    /**
     * Allows only the account owner to create or update encryptionPublicKey.
     * Only 1 encryptionPublicKey is allowed per account, therefore use same set
     * method for both create and update.
     */
    function setEncryptionPublicKey(string _myEncryptionPublicKey) onlyBy(owner) checkBlockLock() returns(bool) {
        encryptionPublicKey = _myEncryptionPublicKey;
        sendEvent(SIG_CHANGE_EVENT, "Encryption key added");
        return true;
    }

    /**
     * Allows only the account owner to create or update signingPublicKey.
     * Only 1 signingPublicKey allowed per account, therefore use same set method
     * for both create and update.
     */
    function setSigningPublicKey(string _mySigningPublicKey) onlyBy(owner) checkBlockLock() returns(bool) {
        signingPublicKey = _mySigningPublicKey;
        sendEvent(SIG_CHANGE_EVENT, "Signing key added");
        return true;
    }

    /**
     * Kills the contract and prevents further actions on it.
     */
    function kill() onlyBy(owner) returns(uint) {
        suicide(owner);
        sendEvent(WARNING_EVENT, "Contract killed");
    }
}
