/*

This contract will be an ERC-721 standrd contract to mint NFT's from the user on the blockchain 


*/

pragma solidity ^0.5.0;

// importing the ERC721Full standard to build and NFT contract
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

// a contract to mint an NFT provided a 
contract MintUrSelf is ERC721Full{

    constructor() public ERC721Full("MintUrSelf" , "MNTME"){}

    struct userInfo {
        string name;
        string minter;
        string secretMsg;
    }

    mapping (uint256 => userInfo) public userMint;

    event storeMessage()

    function mintImage(
            address owner,
            string memory name,
            string memory minter,
            string secretMsg,
            string memory tokenURI
        ) public returns (uint256) {
            uint256 tokenId = totalSupply();

            _mint(owner, tokenId);
            _setTokenURI(tokenId, tokenURI);

            userMint[tokenId] = userInfo(name, minter, secretMsg);

            return tokenId;
        }

    /*
    function decodeMsg (address minter , tokenId) public returns (string){




    }
    */

}
