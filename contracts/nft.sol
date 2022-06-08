/*

This contract will be an ERC-721 standrd contract to mint NFT's from the user on the blockchain 


*/

pragma solidity ^0.5.0;

// importing the ERC721Full standard to build and NFT contract
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

// a contract to mint an NFT provided a 
contract MintUrSelf is ERC721Full{

    constructor() public ERC721Full("MintUrSelf" , "MNTME"){}
    // Defining a struct to store the NFT details
    struct userInfo {
        address owner;
        string name;
        string minter;
        string tokenURI;
        
    }

    mapping (uint256 => userInfo) public userMint;

    // function to mint a token to the user and store the information in the userInfo struct
    function mintImage(
            address owner,
            string memory name,
            string memory minter,
            string memory tokenURI
            
        ) public returns (uint256) {
            uint256 tokenId = totalSupply();

            _mint(owner, tokenId);
            _setTokenURI(tokenId, tokenURI);

            userMint[tokenId] = userInfo(owner ,name, minter , tokenURI);

            return tokenId;
        }

    // write a function to set keep track of all the tokenId's that have been minted with a particular 
   
}